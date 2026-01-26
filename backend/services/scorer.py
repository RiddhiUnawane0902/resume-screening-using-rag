from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from .vector_store import VectorStoreService
import json

class ScorerService:
    def __init__(self):
        self.vector_store_service = VectorStoreService()
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-flash-latest", 
            temperature=0
        )

    def extract_criteria(self, job_description: str) -> list[str]:
        """Extracts key skills and requirements from the JD."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert recruiter. Extract the top 5-10 most critical technical skills or requirements from the following Job Description. Return them as a JSON list of strings."),
            ("human", pd_description := job_description)
        ])
        chain = prompt | self.llm
        try:
            response = chain.invoke({})
            # Naive parsing, better to use JsonOutputParser usually
            content = response.content.strip()
            # Handle potential markdown wrapping
            if content.startswith("```json"):
                content = content[7:-3]
            elif content.startswith("```"):
                content = content[3:-3]
            return json.loads(content)
        except Exception as e:
            print(f"Error extracting criteria: {e}")
            return ["General Requirement"]

    def assess_candidate(self, job_description: str):
        criteria = self.extract_criteria(job_description)
        
        retriever = self.vector_store_service.get_retriever()
        
        strengths = []
        missing = []
        
        # Check each criterion against the resume
        for criterion in criteria:
            # Retrieve relevant docs for this criterion
            docs = retriever.invoke(f"Does the candidate have experience with {criterion}?")
            context = "\n".join([doc.page_content for doc in docs])
            
            # Ask LLM if the criterion is met
            # Ask LLM if the criterion is met
            check_prompt = ChatPromptTemplate.from_messages([
                ("system", "You are evaluating a candidate. Based ONLY on the context provided, determine if the candidate clearly possesses the requirement: '{criterion}'. Return 'YES' or 'NO' and a very brief reason."),
                ("human", "Context:\n{context}\n\nRequirement: {criterion}")
            ])
            res = (check_prompt | self.llm).invoke({"context": context, "criterion": criterion})
            answer = res.content.strip()
            
            if "YES" in answer.upper():
                strengths.append(criterion)
            else:
                missing.append(criterion)
                
        score = int((len(strengths) / len(criteria)) * 100) if criteria else 0
        
        overall_assessment = f"The candidate matches {score}% of the key requirements. "
        if strengths:
            overall_assessment += f"Strong in: {', '.join(strengths[:3])}. "
        if missing:
            overall_assessment += f"Missing experience in: {', '.join(missing[:3])}."

        return {
            "match_score": score,
            "strengths": strengths,
            "missing_skills": missing,
            "overall_assessment": overall_assessment
        }
