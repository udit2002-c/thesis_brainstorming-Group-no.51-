# This file contains templates for prompts used in the thesis generator application

THESIS_BRAINSTORM_PROMPT = """
Generate {num_ideas} thesis ideas in the field of {field_of_study}, focusing on {thesis_type} topics. 
Ensure that the ideas cover a broad range of subfields such as cybersecurity, software engineering, databases, networking, and human-computer interaction. 
Avoid focusing only on artificial intelligence. Use a {tone} writing style.

Format each thesis idea as:
Thesis Idea 1: [Thesis statement]
[Brief explanation of the thesis idea, its significance, and potential research directions]

Thesis Idea 2: [Thesis statement]
[Brief explanation of the thesis idea, its significance, and potential research directions]

...and so on.
"""

# Additional prompts can be added here as the application expands
THESIS_REFINEMENT_PROMPT = """
Refine the following thesis idea: "{thesis_idea}"

Consider the following aspects:
1. Clarity: Is the thesis statement clear and specific?
2. Scope: Is the scope appropriate (not too broad or too narrow)?
3. Significance: Why is this research important?
4. Feasibility: Can this research be conducted with available resources?
5. Originality: How does this contribute new knowledge?

Provide a refined thesis statement and brief explanation.
"""

LITERATURE_REVIEW_PROMPT = """
Generate a brief outline for a literature review on the topic: "{thesis_topic}"

Include:
1. Key areas to explore
2. Foundational works that should be reviewed
3. Potential gaps in the existing literature
4. Methodological approaches to consider
"""