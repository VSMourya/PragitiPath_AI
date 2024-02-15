import React, { useState } from 'react';
import './App.css';

const App = () => {
  const [isStreaming, setIsStreaming] = useState(true);
  const [enableDraw, setEnableDraw] = useState(false);
  const [comment, setComment] = useState('');
  const [comments, setComments] = useState([]);

  const streamSrc = isStreaming ? 'http://127.0.0.1:5000/video_feed' : '';

  const handleToggleStreaming = () => {
    setIsStreaming(!isStreaming);
  };

  const handleToggleDraw = () => {
    setEnableDraw(!enableDraw);
  };

  const handleClear = () => {
    fetch('http://127.0.0.1:5000/clear_circles', { method: 'POST' })
    .then(response => {
      if(response.ok) {
        console.log('Circles cleared');
      }
    })
    .catch(error => console.log('Error:', error));
  };

  const handleSendComment = () => {
    setComments([...comments, comment]);
    setComment('');
  };

  const handleGenerateClick = async () => {
    // Trigger the Flask endpoint to run Python script and get text
    try {
      const response = await fetch('http://127.0.0.1:5000/generate_text', {
        method: 'POST',
      });
      const data = await response.json();
      // Update your textarea (assuming you have a state for it)
      document.querySelector('.caption-textbox').value = data.text; // Or use a state setter
    } catch (error) {
      console.error('Error fetching text:', error);
    }
  };
  
  const handleToggleDrawFun = async () => {
    setEnableDraw(!enableDraw);
  
    if (!enableDraw) { // If enabling draw, start speech to text
      try {
        await fetch('http://127.0.0.1:5000/start_speech_to_text', { method: 'POST' });
        console.log('Speech to text started');
      } catch (error) {
        console.error('Error starting speech to text:', error);
      }
    } else { // If disabling draw, stop speech to text
      try {
        await fetch('http://127.0.0.1:5000/stop_speech_to_text', { method: 'POST' });
        console.log('Speech to text stopped');
      } catch (error) {
        console.error('Error stopping speech to text:', error);
      }
    }
  };

  return (
    <div className="app">
      <header className="header">PragatiPath AI</header>

      <div className="main-container">
        <div className="video-and-controls">
          <div className="video-container">
            {isStreaming ? (
              <img src={streamSrc} alt="Video Feed" style={{ width: '100%', height: 'auto' }} />
            ) : (
              <div className="video-placeholder">Stream Paused</div>
            )}
          </div>
          
          <div className="controls">
            <button onClick={handleToggleStreaming} className={isStreaming ? 'pause' : 'resume'}>
              {isStreaming ? 'Pause' : 'Resume'}
            </button>
            <label className="switch">
              <input type="checkbox" checked={enableDraw} onChange={handleToggleDrawFun} />
              <span className="slider round"></span>
            </label>
            <button onClick={handleClear} className="clear">Clear</button>
          </div>

          
        </div>

        <div className="comments-section">
          <div className="comments-display">
            {comments.map((c, index) => (
              <div key={index} className="comment">{c}</div>
            ))}
          </div>
          <textarea value={comment} onChange={(e) => setComment(e.target.value)} className="comment-box" placeholder="Type your comment..."></textarea>
          <button onClick={handleSendComment} className="send">Send</button>

          <div className="caption-container">
            <textarea placeholder="Live caption..." className="caption-textbox"></textarea>
            <button onClick={handleGenerateClick} className="generate">Generate</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
