from openai import OpenAI
import config
import json

class OpenAIService:
    def __init__(self):
        # Detect if it's a Groq key
        api_key = config.OPENAI_API_KEY
        base_url = None
        if api_key and api_key.startswith("gsk_"):
            base_url = "https://api.groq.com/openai/v1"
            self.model = "llama-3.3-70b-versatile"
        else:
            self.model = "gpt-3.5-turbo"
            
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        ) if api_key and api_key != "sk-..." else None

    def is_configured(self):
        return self.client is not None

    def get_career_recommendation(self, interests, skills, preferred_field):
        """
        Generates personalized career recommendations based on user inputs.
        """
        if not self.is_configured():
            return {
                "error": "OpenAI API key is not configured. Please set OPENAI_API_KEY in .env file."
            }

        prompt = f"""
        Act as an expert career counselor. Based on the following student profile:
        - Interests: {interests}
        - Skills: {skills}
        - Preferred Field: {preferred_field}

        Provide 3 specific career recommendations, such as Software Engineering, Data Science, Cybersecurity, UI/UX Design, or Cloud Computing.
        For each recommendation, give a brief, personalized explanation of why it fits and a list of required skills/technologies.
        
        Also include 3 suggested online courses or certifications they should pursue to get started in this field. 
        Each course MUST include a real, functional URL from a platform like Coursera, Udemy, or edX.

        Format the response as JSON with the following structure:
        {{
            "recommendations": [
                {{
                    "title": "Career Title",
                    "explanation": "Why it's a good fit",
                    "skills_required": ["Skill 1", "Skill 2"]
                }}
            ],
            "recommended_courses": [
                {{
                    "title": "Course/Certification Name",
                    "description": "Brief description",
                    "url": "https://official-domain.com/path",
                    "platform": "Coursera/Udemy/etc."
                }}
            ]
        }}
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful career counselor that outputs structured JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return {"error": str(e)}

    def chat_with_counselor(self, messages):
        """
        Sends chat history to OpenAI to get the next response.
        Messages should be a list of dicts with 'role' and 'content'.
        """
        if not self.is_configured():
            return "OpenAI API key is not configured. I am running in offline mode. Please set `OPENAI_API_KEY`."

        system_prompt = {
            "role": "system", 
            "content": "You are a friendly, encouraging, and highly knowledgeable academic and career counselor. Answer student questions about academic choices, career paths, offer study tips, and provide motivational guidance. Keep responses concise, professional, and warmly encouraging."
        }
        
        # Prepend system prompt to the message history
        full_messages = [system_prompt] + messages

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=full_messages,
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return f"I'm sorry, I'm having trouble connecting to my brain right now. Error: {str(e)}"

    def get_resource_recommendations(self, topic):
        """Generates structured resource recommendations based on a topic."""
        prompt = f"""
        Act as an expert academic and career advisor. Provide a deep list of HIGH-QUALITY, VERIFIED learning resources for: "{topic}".
        
        You MUST provide exactly 15 recommendations for EACH of the following categories (60 items total):
        1. Courses (Only from official platforms: Coursera, Udemy, edX, LinkedIn Learning, Khan Academy)
        2. YouTube (Direct links to popular educational channels or specific viral tutorials like FreeCodeCamp, Fireship, Traversy Media, etc.)
        3. Books (Real titles found on Amazon, O'Reilly, or GoodReads)
        4. Certifications (Official vendor certs: AWS, Google, Microsoft, CompTIA, Cisco)

        CRITICAL REQUIREMENT: Every 'url' MUST be a REAL, FUNCTIONAL web address. 
        - DO NOT hallucinate or "guess" URLs using slugs.
        - If you do not know the exact deep-link URL, providing the official homepage/search results for that resource on the platform (e.g. coursera.org/search?query=...) is better than a fake link.
        - YouTube links MUST follow standard formats (e.g. https://www.youtube.com/c/ChannelName or https://www.youtube.com/watch?v=...)
        - NO placeholder links like 'example.com' or 'yourlinkhere.com'.

        Format your response EXACTLY as a Python list of dictionaries:
        [
            {{"category": "Courses", "title": "Real Course Name", "platform": "Platform", "desc": "Concise info", "url": "https://official-domain.com/path"}},
            ...
        ]
        Only return the list, no other text. Verify every single URL looks realistic and is hosted on the correct domain.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional educational resource curator. You NEVER hallucinate links. Every URL you provide must be verified and real. Return only a Python-parseable list of dictionaries."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            content = response.choices[0].message.content.strip()
            # Basic cleaning in case the AI adds markdown blocks
            if content.startswith("```python"):
                content = content[9:-3].strip()
            elif content.startswith("```"):
                content = content[3:-3].strip()
                
            import ast
            return ast.literal_eval(content)
        except Exception as e:
            print(f"Error in resource recommendation: {e}")
            return None

    def get_academic_advice(self, subjects_data):
        """
        Analyzes subject marks to find risk subjects and generate improvement plans.
        subjects_data format: {'Math': 45, 'Science': 80, ...}
        """
        if not self.is_configured():
            return {
                "error": "OpenAI API key is not configured."
            }

        prompt = f"""
        Act as an expert academic advisor. The student has provided the following marks out of 100 for their subjects:
        {json.dumps(subjects_data, indent=2)}

        Analyze these marks to identify "at-risk" subjects (generally subjects with low scores, e.g., below 60 or the lowest relative to others). 
        For each at-risk subject, provide:
        - A brief analysis of why it might be challenging.
        - A step-by-step action plan or learning path to boost their grade in that specific subject.

        Format the response EXACTLY as a JSON object with this structure:
        {{
            "overall_assessment": "A brief encouraging summary of their overall performance.",
            "risk_subjects": [
                {{
                    "subject": "Subject Name",
                    "current_mark": 45,
                    "analysis": "Brief analysis",
                    "action_plan": [
                        "Action item 1",
                        "Action item 2"
                    ]
                }}
            ],
            "general_advice": "A short closing motivational tip or study strategy."
        }}
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful academic advisor. Output structured JSON only."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return {"error": str(e)}

    def analyze_resume(self, resume_text, role):
        """
        Analyzes a resume against a target job role.
        Returns match score, strengths, skill gaps, and recommendations.
        """
        if not self.is_configured():
            return {"error": "OpenAI API key is not configured."}

        prompt = f"""
        You are an expert HR recruiter and career coach. Analyze the following resume against the target job role: "{role}".

        Resume Text:
        ---
        {resume_text[:4000]}
        ---

        Provide a thorough, honest, and actionable analysis. Return EXACTLY this JSON structure:
        {{
            "match_score": <integer 0-100 indicating overall fit for the role>,
            "summary": "2-3 sentence executive summary of the candidate's profile vs the role.",
            "strengths": [
                "Specific strength 1 relevant to the role",
                "Specific strength 2",
                "Specific strength 3"
            ],
            "skill_gaps": [
                "Missing skill or experience 1",
                "Missing skill or experience 2"
            ],
            "recommendations": [
                "Concrete actionable improvement 1",
                "Concrete actionable improvement 2",
                "Concrete actionable improvement 3"
            ],
            "keywords_missing": ["keyword1", "keyword2"],
            "ats_tips": "A short tip to improve ATS compatibility for this specific role."
        }}
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert resume reviewer and HR specialist. Output structured JSON only."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.6
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error in analyze_resume: {e}")
            return {"error": str(e)}

    def get_interview_questions(self, role):
        """
        Generates important interview questions for a given job role.
        Returns categorized questions with tips.
        """
        if not self.is_configured():
            return {"error": "OpenAI API key is not configured."}

        prompt = f"""
        You are a senior interviewer and career coach. Generate the most important and commonly asked
        interview questions for the role: "{role}".

        Return EXACTLY this JSON structure:
        {{
            "role_summary": "One sentence describing what this role is about.",
            "technical": [
                {{"question": "Question text", "tip": "What interviewers look for in the answer"}}
            ],
            "behavioral": [
                {{"question": "Situation/behavior question", "tip": "Tip for answering this"}}
            ],
            "role_specific": [
                {{"question": "Domain-specific question", "tip": "Key points to cover"}}
            ],
            "situational": [
                {{"question": "What would you do if... scenario", "tip": "How to structure the answer"}}
            ]
        }}

        Rules:
        - Provide exactly 5 questions per category (20 total).
        - Make questions specific and realistic for "{role}".
        - Tips should be concise and actionable (1–2 sentences).
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert interviewer. Output structured JSON only."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error in get_interview_questions: {e}")
            return {"error": str(e)}

# Create a singleton instance
try:
    ai_service = OpenAIService()
except Exception as e:
    print(f"FAILED TO INITIALIZE AI SERVICE: {e}")
    ai_service = None
