import re
import logging
from typing import Dict, List, Tuple, Optional

class AIEnhancementService:
    def __init__(self):
        # Initialize a service with advanced text processing capabilities
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Common professional action verbs for resume enhancement
        self.action_verbs = [
            "achieved", "accelerated", "accomplished", "administered", "advanced", "analyzed",
            "built", "collaborated", "conducted", "created", "delivered", "designed", "developed",
            "established", "executed", "expanded", "generated", "implemented", "improved", "increased",
            "launched", "led", "managed", "optimized", "orchestrated", "organized", "pioneered",
            "reduced", "resolved", "revitalized", "spearheaded", "streamlined", "strengthened",
            "transformed", "unified", "utilized", "validated"
        ]
    
    def enhance_description(self, text: str) -> str:
        """
        Enhance a professional experience description with improved language and structure.
        
        Args:
            text (str): Original experience description

        Returns:
            str: Enhanced professional description
        """
        if not text:
            self.logger.warning("Received empty text for enhancement")
            return ""

        try:
            # Process and enhance the text
            cleaned_text = self._clean_text(text)
            structured_text = self._structure_content(cleaned_text)
            enhanced_text = self._apply_professional_enhancement(structured_text)
            return enhanced_text
            
        except Exception as e:
            self.logger.error(f"Error enhancing description: {str(e)}")
            return text
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize the input text."""
        # Remove extra whitespace
        cleaned = re.sub(r'\s+', ' ', text).strip()
        # Fix common punctuation issues
        cleaned = re.sub(r'\s+([.,;:!?])', r'\1', cleaned)
        return cleaned
    
    def _structure_content(self, text: str) -> str:
        """Add structure to the content if needed."""
        # If text is very long, try to break it into bullet points
        if len(text) > 200 and '\n' not in text and '•' not in text:
            sentences = re.split(r'(?<=[.!?])\s+', text)
            if len(sentences) > 2:
                # Convert sentences to bullet points
                return '\n'.join([f"• {s}" for s in sentences if len(s) > 10])
        return text
    
    def _apply_professional_enhancement(self, text: str) -> str:
        """Apply professional enhancements to the text."""
        # If text doesn't have bullet points, add a professional prefix
        if not text.startswith('•') and not text.startswith('-'):
            prefix = "Professional Experience: "
            if not text.startswith(prefix):
                text = prefix + text
        
        # Replace weak verbs with strong action verbs
        text = self._strengthen_verbs(text)
        
        # Add quantifiable achievements if possible
        text = self._add_quantifiers(text)
        
        return text
    
    def _strengthen_verbs(self, text: str) -> str:
        """Replace weak verbs with strong action verbs."""
        weak_verb_patterns = [
            (r'(?i)\b(did|made|worked on|helped with|was responsible for)\b', self.action_verbs),
            (r'(?i)\b(used|utilized|employed)\b', ["leveraged", "implemented", "deployed"]),
            (r'(?i)\b(improved|made better)\b', ["enhanced", "optimized", "streamlined", "revitalized"]),
        ]
        
        enhanced_text = text
        for pattern, replacements in weak_verb_patterns:
            matches = re.findall(pattern, enhanced_text)
            for match in matches:
                # Choose a replacement verb based on position in the list (deterministic)
                index = sum(ord(c) for c in match) % len(replacements)
                enhanced_text = re.sub(f"\b{match}\b", replacements[index], enhanced_text, count=1, flags=re.IGNORECASE)
        
        return enhanced_text
    
    def _add_quantifiers(self, text: str) -> str:
        """Add quantifiable achievements if they're not already present."""
        # Check if text already has numbers (likely already quantified)
        if re.search(r'\d+%|\d+\s*x', text):
            return text
            
        # Look for improvement-related terms without quantifiers
        improvement_patterns = [
            (r'(?i)\b(improved|increased|enhanced|boosted)\b[^.,]*?\b(performance|efficiency|productivity)\b', 
             r'\1\2 by approximately 20%'),
            (r'(?i)\b(reduced|decreased|minimized)\b[^.,]*?\b(costs|expenses|time|errors)\b',
             r'\1\2 by approximately 15%'),
        ]
        
        enhanced_text = text
        for pattern, replacement_template in improvement_patterns:
            match = re.search(pattern, enhanced_text)
            if match:
                original = match.group(0)
                # Only replace if it doesn't already have a number
                if not re.search(r'\d+', original):
                    replacement = re.sub(pattern, replacement_template, original)
                    enhanced_text = enhanced_text.replace(original, replacement)
        
        return enhanced_text
        
    def extract_skills(self, text: str) -> List[Dict[str, any]]:
        """
        Extract skills from resume text and categorize them.
        
        Args:
            text (str): Resume text
            
        Returns:
            List[Dict]: List of skills with name and estimated level
        """
        # Common skill categories and keywords
        skill_categories = {
            'technical': [
                'python', 'java', 'javascript', 'html', 'css', 'sql', 'react', 'angular', 'vue', 'node', 
                'django', 'flask', 'spring', 'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'git',
                'machine learning', 'ai', 'data science', 'tensorflow', 'pytorch', 'pandas', 'numpy',
                'c++', 'c#', 'php', 'ruby', 'swift', 'kotlin', 'rust', 'go', 'scala', 'r'
            ],
            'management': [
                'project management', 'agile', 'scrum', 'kanban', 'lean', 'prince2', 'pmp', 'waterfall',
                'budgeting', 'resource allocation', 'risk management', 'strategic planning', 'team management',
                'stakeholder management', 'vendor management', 'client management', 'product management'
            ],
            'leadership': [
                'team leadership', 'mentoring', 'coaching', 'conflict resolution', 'decision making',
                'delegation', 'motivation', 'team building', 'change management', 'performance management',
                'talent development', 'executive leadership', 'vision setting', 'cross-functional leadership'
            ]
        }
        
        extracted_skills = []
        
        # Look for skills in the text
        for category, skills in skill_categories.items():
            for skill in skills:
                # Use word boundaries to find whole words/phrases
                pattern = r'\b' + re.escape(skill) + r'\b'
                if re.search(pattern, text.lower()):
                    # Calculate a confidence level based on context
                    confidence = self._calculate_skill_level(text, skill)
                    extracted_skills.append({
                        'name': skill.title(),  # Capitalize skill name
                        'category': category,
                        'level': confidence
                    })
        
        return extracted_skills
    
    def _calculate_skill_level(self, text: str, skill: str) -> int:
        """Calculate an estimated skill level based on context."""
        # Base level
        level = 70
        
        # Look for expertise indicators
        expertise_indicators = [
            (r'\b(expert|proficient|advanced|specialist)\b[^.]*\b' + re.escape(skill) + r'\b', 20),
            (r'\b' + re.escape(skill) + r'\b[^.]*\b(expert|proficient|advanced)\b', 20),
            (r'\b(experience|years)\b[^.]*\b' + re.escape(skill) + r'\b', 15),
            (r'\b(certified|qualification)\b[^.]*\b' + re.escape(skill) + r'\b', 25),
            (r'\b(beginner|basic|elementary)\b[^.]*\b' + re.escape(skill) + r'\b', -20),
        ]
        
        for pattern, adjustment in expertise_indicators:
            if re.search(pattern, text.lower()):
                level += adjustment
        
        # Ensure level is within bounds
        return max(50, min(level, 98))  # Keep between 50-98%
    
    def extract_contact_info(self, text: str) -> Dict[str, str]:
        """Extract contact information from resume text."""
        contact_info = {}
        
        # Extract email
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        if email_match:
            contact_info['email'] = email_match.group(0)
        
        # Extract phone number (various formats)
        phone_match = re.search(r'\b(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b', text)
        if phone_match:
            contact_info['phone'] = phone_match.group(0)
        
        # Extract LinkedIn
        linkedin_match = re.search(r'linkedin\.com/in/[\w-]+', text.lower())
        if linkedin_match:
            contact_info['linkedin'] = 'https://' + linkedin_match.group(0)
        
        # Extract website/portfolio
        website_match = re.search(r'\b(?:https?://)?(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?\b', text)
        if website_match and not (website_match.group(0).startswith('linkedin') or 'linkedin.com' in website_match.group(0)):
            url = website_match.group(0)
            if not url.startswith('http'):
                url = 'https://' + url
            contact_info['website'] = url
        
        return contact_info