# IntelliSupport Streamlit Frontend

A modern Streamlit-based frontend for the IntelliSupport intelligent customer support system.

## Features

- 💬 **Interactive Chat Interface** - Clean, responsive chat UI
- 📊 **Real-time Analytics** - Conversation insights and metrics
- ⚙️ **Configuration Management** - Easy settings adjustment
- 🔍 **Debug Mode** - Detailed response metadata
- 📱 **Responsive Design** - Works on desktop and mobile
- 🎨 **Modern UI** - Beautiful, professional interface

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python run.py
   ```
   
   Or directly with Streamlit:
   ```bash
   streamlit run app.py
   ```

3. **Access the Application**
   - Open your browser to `http://localhost:8501`
   - Start chatting with IntelliSupport!

## Project Structure

```
frontend/
├── app.py                 # Main Streamlit app
├── run.py                # Application runner
├── requirements.txt      # Python dependencies
├── components/           # UI components
│   ├── chat_interface.py # Main chat interface
│   ├── sidebar.py       # Sidebar with controls
│   └── header.py        # Application header
├── utils/               # Utility modules
│   ├── api_client.py    # Backend API client
│   ├── config.py        # Configuration management
│   ├── session_state.py # Streamlit session state
│   └── message_handler.py # Message processing
├── pages/               # Additional pages
│   ├── analytics.py     # Analytics dashboard
│   └── settings.py      # Settings page
└── assets/             # Static assets
```

## Configuration

The frontend automatically loads configuration from `../config.yaml`. Key settings include:

- **API Backend**: Configure the backend API endpoint
- **UI Settings**: Theme, debug mode, auto-scroll
- **Model Selection**: Choose different LLM models
- **Display Options**: Message limits, formatting preferences

## Features

### Chat Interface
- Real-time messaging with the AI agent
- Message history and conversation tracking
- Typing indicators and loading states
- Debug information display

### Analytics Dashboard
- Conversation volume trends
- Intent classification statistics
- Sentiment analysis results
- Response time metrics
- User satisfaction scores

### Settings Panel
- LLM model configuration
- Retrieval system settings
- Safety and PII options
- UI customization options

## API Integration

The frontend communicates with the IntelliSupport backend API:

- **Endpoint**: `POST /api/chat`
- **Fallback**: Mock responses when backend unavailable
- **Error Handling**: Graceful degradation and error messages

## Development

### Adding New Components

1. Create component in `components/` directory
2. Import and use in `app.py` or other components
3. Follow Streamlit component patterns

### Adding New Pages

1. Create page in `pages/` directory
2. Use `st.set_page_config()` for page settings
3. Implement main function with page logic

### Customizing Styling

- Use Streamlit's theming system
- Add custom CSS with `st.markdown()` and `unsafe_allow_html=True`
- Configure colors in `run.py` theme settings

## Environment Variables

Optional environment variables:

```bash
INTELLISUPPORT_API_URL=http://localhost:8000  # Backend API URL
INTELLISUPPORT_DEBUG=true                     # Enable debug mode
STREAMLIT_SERVER_PORT=8501                    # Server port
```

## Troubleshooting

### Backend Connection Issues
- Ensure backend is running on configured port
- Check API URL in settings
- Frontend provides mock responses when backend unavailable

### Performance Issues
- Clear browser cache
- Restart Streamlit server
- Check message history limits in settings

### UI Issues
- Try different browser
- Clear Streamlit cache with `Ctrl+R`
- Check browser console for JavaScript errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
