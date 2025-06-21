# This file contains templates for prompts used in the thesis generator application
import random

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

def get_prompt_template(research_field: str, num_ideas: int, tone: str, thesis_type: str) -> str:
    """Generate a formatted prompt for the AI API"""
    return f"Generate {num_ideas} {thesis_type} thesis ideas in the field of {research_field}. Use a {tone} tone. Make the ideas specific and innovative. Format each idea with a number and a brief explanation."

def generate_mock_ideas(research_field: str, num_ideas: int, tone: str, thesis_type: str) -> str:
    """Generate intelligent mock thesis ideas as fallback"""
    
    # Enhanced thesis templates by field and type
    templates = {
        "machine learning": {
            "argumentative": [
                "Federated Learning Privacy-Preservation is Essential for Healthcare AI Adoption",
                "Explainable AI Should Be Mandatory for Financial Decision-Making Systems",
                "Quantum Machine Learning Will Revolutionize Drug Discovery Processes"
            ],
            "analytical": [
                "Decomposing the Impact of Bias in Facial Recognition Systems Across Demographics",
                "Analyzing the Convergence Properties of Neural Architecture Search Algorithms",
                "Examining the Trade-offs Between Model Accuracy and Computational Efficiency in Edge AI"
            ],
            "expository": [
                "Understanding the Mathematical Foundations of Transformer Architecture",
                "Exploring the Evolution of Reinforcement Learning from Q-Learning to Deep RL",
                "Illuminating the Role of Attention Mechanisms in Natural Language Processing"
            ],
            "comparative": [
                "Comparing Supervised vs. Unsupervised Learning Approaches for Anomaly Detection",
                "Contrasting Classical Optimization with Evolutionary Algorithms in Neural Network Training",
                "Evaluating Centralized vs. Decentralized Learning in Multi-Agent Systems"
            ]
        },
        "computer science": {
            "argumentative": [
                "Blockchain Technology is Overhyped and Unsuitable for Most Enterprise Applications",
                "Open Source Software Development Models Produce Higher Quality Code Than Proprietary Methods",
                "Quantum Computing Will Make Current Cryptographic Standards Obsolete Within a Decade"
            ],
            "analytical": [
                "Analyzing the Scalability Bottlenecks in Distributed Database Systems",
                "Examining the Security Vulnerabilities in Internet of Things (IoT) Networks",
                "Decomposing the Performance Trade-offs in Microservices Architecture"
            ],
            "expository": [
                "Understanding the Principles of Distributed Consensus Algorithms",
                "Exploring the Evolution of Programming Paradigms from Procedural to Functional",
                "Illuminating the Role of Compilers in Modern Software Development"
            ],
            "comparative": [
                "Comparing SQL vs. NoSQL Database Performance in Big Data Applications",
                "Contrasting Agile vs. Waterfall Methodologies in Large-Scale Software Projects",
                "Evaluating Cloud vs. Edge Computing for Real-Time Data Processing"
            ]
        },
        "cybersecurity": {
            "argumentative": [
                "Zero Trust Architecture is the Only Viable Security Model for Modern Enterprises",
                "Biometric Authentication Systems Create More Security Risks Than They Solve",
                "Artificial Intelligence in Cybersecurity Will Replace Human Security Analysts"
            ],
            "analytical": [
                "Analyzing the Attack Vectors in 5G Network Infrastructure",
                "Examining the Effectiveness of Machine Learning in Malware Detection",
                "Decomposing the Root Causes of Data Breaches in Healthcare Organizations"
            ],
            "expository": [
                "Understanding the Technical Mechanisms of Advanced Persistent Threats",
                "Exploring the Cryptographic Principles Behind Secure Communication Protocols",
                "Illuminating the Role of Social Engineering in Modern Cyber Attacks"
            ],
            "comparative": [
                "Comparing Signature-Based vs. Behavior-Based Intrusion Detection Systems",
                "Contrasting Public Key vs. Symmetric Key Cryptography for Different Use Cases",
                "Evaluating Network-Based vs. Host-Based Security Monitoring Approaches"
            ]
        }
    }
    
    # Methodology templates
    methodologies = [
        "Literature review, empirical analysis, and case study methodology",
        "Mixed-methods approach combining quantitative analysis and qualitative interviews",
        "Experimental design with control groups and statistical validation",
        "Systematic literature review and meta-analysis of existing research",
        "Prototype development and comparative performance evaluation",
        "Survey research and statistical modeling techniques"
    ]
    
    # Contribution templates
    contributions = [
        "providing new theoretical frameworks for understanding complex systems",
        "developing novel algorithms with improved efficiency and accuracy",
        "establishing best practices for industry implementation",
        "bridging the gap between theoretical research and practical applications",
        "offering comprehensive solutions to persistent challenges in the field",
        "advancing the state-of-the-art through innovative methodological approaches"
    ]
    
    # Get appropriate templates
    field_key = research_field.lower()
    if field_key not in templates:
        field_key = "computer science"  # Default fallback
    
    type_key = thesis_type.lower()
    if type_key not in templates[field_key]:
        type_key = "argumentative"  # Default fallback
    
    ideas = templates[field_key][type_key]
    
    # Generate the specified number of ideas
    result = ""
    for i in range(min(num_ideas, len(ideas))):
        idea = ideas[i]
        methodology = random.choice(methodologies)
        contribution = random.choice(contributions)
        
        result += f"\n**Thesis Idea {i+1}: {idea}**\n\n"
        result += f"**Research Overview:** This {thesis_type} thesis addresses a critical challenge in {research_field} by examining the theoretical foundations and practical implications of the proposed research question. The study will investigate current methodologies, identify gaps in existing literature, and propose innovative solutions that advance both academic understanding and industry applications.\n\n"
        result += f"**Methodology:** {methodology}. The research will employ rigorous data collection techniques, statistical analysis, and validation through peer review and expert consultation.\n\n"
        result += f"**Expected Contributions:** This research will contribute to {research_field} by {contribution}. The findings will have significant implications for both researchers and practitioners in the field.\n\n"
        result += "---\n"
    
    return result