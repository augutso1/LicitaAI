# Overview

Licita-IA is a web-based AI application that automates procurement processes for government tenders (licitações). The application provides a chat-like interface where users can describe products they need to quote, and an AI agent performs automated research and analysis to find compatible products and vendors. The system simulates a multi-step procurement workflow with real-time status updates displayed through a streaming interface.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Framework**: Streamlit - chosen for rapid prototyping and simple deployment of data-driven web applications
- **Interface Pattern**: Single-page chat application with real-time streaming responses
- **Layout**: Centered layout with collapsed sidebar for minimal distraction
- **Theme**: Custom dark theme implementation using CSS injection for professional appearance

## UI/UX Design Decisions
- **Chat Interface**: Uses `st.chat_input` for authentic messaging experience with placeholder text guiding user input
- **Streaming Simulation**: Mock implementation of AI agent workflow with step-by-step status updates to show processing progress
- **Visual Feedback**: Custom CSS styling with hover effects and transitions for better user interaction
- **Color Scheme**: Dark theme with gray backgrounds (#262730) and light text (#FAFAFA) for professional government/business context

## Application Flow
- **Welcome State**: Displays initial greeting message when application starts
- **User Input Processing**: Captures product descriptions through chat input
- **Response Streaming**: Simulates multi-step AI workflow with status updates:
  1. Agent activation
  2. Web scraping for products/suppliers
  3. Compatibility analysis and CNPJ verification
  4. Additional processing steps
- **Real-time Updates**: Uses time delays and iterative message updates to simulate live processing

## Code Organization
- **Single File Architecture**: All functionality contained in `app.py` for simplicity
- **CSS Injection**: Custom styling applied through `st.markdown` with embedded CSS
- **Mock Data Layer**: Simulated responses and status messages for demonstration purposes

# External Dependencies

## Core Framework
- **Streamlit**: Web application framework for the user interface
- **Python Standard Library**: 
  - `time` module for simulating processing delays
  - `random` module for potential response variation

## Planned Integrations
- **AI/ML Services**: Backend AI agents for actual product research and analysis
- **Web Scraping Infrastructure**: For gathering product and supplier information
- **CNPJ Validation Services**: For verifying Brazilian company registration numbers
- **Government Procurement APIs**: For accessing official tender and supplier databases

## Browser Dependencies
- Modern web browser with JavaScript enabled for Streamlit functionality
- CSS3 support for custom styling and animations