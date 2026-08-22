'use client';
import { useState, useEffect, useRef } from 'react';
import { useBroadcastChannel } from '@/hooks/useBroadcastChannel';

export default function Receiver() {
  const [connectionQuality, setConnectionQuality] = useState('full');
  const [messages, setMessages] = useState<any[]>([]);
  const [currentView, setCurrentView] = useState('home');
  const [selectedMsg, setSelectedMsg] = useState(0);
  const [isRecording, setIsRecording] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [battery, setBattery] = useState(92);
  const [mode, setMode] = useState('live');
  const [apiUrl, setApiUrl] = useState('http://127.0.0.1:8000');
  
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const mediaRecorder = useRef<MediaRecorder | null>(null);
  const audioChunks = useRef<Blob[]>([]);

  const { postMessage } = useBroadcastChannel('dadaai_channel', (msg) => {
    if (msg.type === 'CONFIG_CHANGED') loadSettings();
    if (msg.type === 'CONNECTION_QUALITY') setConnectionQuality(msg.quality);
    if (msg.type === 'LIVE_SMS_ARRIVED') receiveLiveMessage(msg);
    if (msg.type === 'SMS_SENT') processMockSMS(msg.text);
  });

  const loadSettings = () => {
    setMode(localStorage.getItem('dadaai_api_mode') || 'live');
    setApiUrl(localStorage.getItem('dadaai_backend_url') || 'http://127.0.0.1:8000');
    setConnectionQuality(localStorage.getItem('dadaai_connection_quality') || 'full');
  };

  useEffect(() => {
    loadSettings();
    const timer = setInterval(() => setBattery(b => Math.max(0, b - 1)), 600000);
    return () => clearInterval(timer);
  }, []);

  const receiveLiveMessage = (data: any) => {
    const shouldSpeak = connectionQuality === 'full';
    const newMsg = {
      original: data.original,
      display: data.display,
      time: new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' }),
      wasAI: true,
      liveVoice: shouldSpeak
    };
    setMessages(prev => [...prev, newMsg]);
    
    if (shouldSpeak) deliverToScreen(data.display, true, newMsg);
    else deliverToScreen(data.display, false, newMsg);
  };

  const processMockSMS = (text: string) => {
    const newMsg = { original: text, display: text, time: new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' }), wasAI: false, liveVoice: false };
    setMessages(prev => [...prev, newMsg]);
    deliverToScreen(text, connectionQuality === 'full', newMsg);
  };

  const deliverToScreen = (content: string, shouldSpeak: boolean, msg: any) => {
    setCurrentView('reading');
    setSelectedMsg(messages.length); // will point to the new msg index
    
    if (shouldSpeak) {
      if (mode === 'live') setTimeout(() => streamTTSFromBackend(content), 800);
      else setTimeout(() => speakBrowserTTS(content), 800);
    }
  };

  const streamTTSFromBackend = async (text: string) => {
    stopAudio();
    setIsSpeaking(true);
    try {
      const res = await fetch(`${apiUrl}/api/v1/voice/tts`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, language: 'hi' })
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const blob = await res.blob();
      const audio = new Audio(URL.createObjectURL(blob));
      audio.onended = () => setIsSpeaking(false);
      audio.onerror = () => setIsSpeaking(false);
      audio.play();
      audioRef.current = audio;
    } catch (err) {
      setIsSpeaking(false);
      speakBrowserTTS(text);
    }
  };

  const speakBrowserTTS = (text: string) => {
    stopAudio();
    setIsSpeaking(true);
    const u = new SpeechSynthesisUtterance(text);
    u.lang = 'hi-IN';
    u.rate = 0.9;
    u.onend = () => setIsSpeaking(false);
    window.speechSynthesis.speak(u);
  };

  const stopAudio = () => {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current = null;
    }
    window.speechSynthesis.cancel();
    setIsSpeaking(false);
  };

  const handleVoiceAI = async () => {
    if (isRecording) return;
    stopAudio();
    setIsRecording(true);
    
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
      mediaRecorder.current = recorder;
      audioChunks.current = [];
      
      recorder.ondataavailable = (e) => audioChunks.current.push(e.data);
      recorder.onstop = async () => {
        setIsRecording(false);
        const blob = new Blob(audioChunks.current, { type: 'audio/webm' });
        
        if (mode === 'live' && connectionQuality === 'full') {
          setCurrentView('processing');
          try {
            const formData = new FormData();
            formData.append('audio', blob, 'voice.webm');
            formData.append('language', 'hi');
            formData.append('phone_number', '+919876543210');
            
            const res = await fetch(`${apiUrl}/api/v1/voice/process`, {
              method: 'POST', body: formData
            });
            if (!res.ok) throw new Error('API Error');
            const resBlob = await res.blob();
            const audio = new Audio(URL.createObjectURL(resBlob));
            setIsSpeaking(true);
            audio.onended = () => { setIsSpeaking(false); setCurrentView('home'); };
            audio.play();
            audioRef.current = audio;
          } catch (e) {
            setCurrentView('home');
            speakBrowserTTS("माफ़ करना, सर्वर से संपर्क नहीं हो पा रहा है।");
          }
        } else {
          setCurrentView('home');
          speakBrowserTTS("बैटरी 92 प्रतिशत है।");
        }
      };
      
      recorder.start();
      setTimeout(() => {
        if (mediaRecorder.current && mediaRecorder.current.state === 'recording') {
          mediaRecorder.current.stop();
          stream.getTracks().forEach(t => t.stop());
        }
      }, 4000);
      
    } catch (err) {
      setIsRecording(false);
      console.error(err);
    }
  };

  const navigate = (dir: string) => {
    if (currentView === 'reading') {
      if (dir === 'back') {
        stopAudio();
        setCurrentView('home');
      }
    }
  };

  return (
    <div className="bg-[#1a1025] min-h-screen text-slate-200 flex flex-col items-center p-6">
      <div className="text-center mb-6">
        <span className="text-xs font-semibold text-purple-400 tracking-wider uppercase">
          <i className="fas fa-phone-alt mr-1"></i> Dada Ji's Phone (2G)
        </span>
      </div>

      <div className="feature-phone">
        <div className="flex justify-center gap-0.5 mb-2">
          <div className="w-1 h-1 rounded-full bg-gray-600"></div><div className="w-10 h-1 rounded-full bg-gray-600"></div><div className="w-1 h-1 rounded-full bg-gray-600"></div>
        </div>

        <div className="lcd-screen relative overflow-hidden" style={{ minHeight: '180px' }}>
          {isSpeaking && <div className="absolute inset-0 border-4 border-green-500/50 rounded-lg animate-pulse z-0 pointer-events-none"></div>}
          
          <div className="lcd-header flex justify-between px-2 pt-1 text-[10px] z-10 relative bg-[#c8d4a4]">
            <div className="flex gap-1"><i className="fas fa-signal"></i><i className="fas fa-signal"></i></div>
            <div className="font-bold">DadaAI</div>
            <div className="flex items-center"><i className="fas fa-battery-three-quarters mr-1"></i> {battery}%</div>
          </div>

          <div className="h-full px-2 pt-4 pb-2 z-10 relative">
            {
              currentView === 'home' ? (
                <div className="text-center mt-6">
                  <div className="text-2xl text-yellow-600 mb-2">🙏</div>
                  <h2 className="text-lg font-bold text-gray-800">नमस्ते दादा जी</h2>
                  <div className="text-[10px] text-gray-600 font-bold mt-1">DadaAI Ready</div>
                  <div className="text-xs text-gray-700 mt-4 font-semibold">{
                    messages.length > 0 ? `${messages.length} संदेश` : 'कोई नया संदेश नहीं'
                  }</div>
                </div>
              ) : currentView === 'processing' ? (
                <div className="text-center mt-8">
                  <i className="fas fa-circle-notch fa-spin text-2xl text-purple-700 mb-2"></i>
                  <div className="text-xs font-bold text-gray-800">सुन रहा हूँ...</div>
                </div>
              ) : currentView === 'reading' && messages[selectedMsg] ? (
                <div className="text-center pt-2">
                  <div className="text-xl text-green-600"><i className="fas fa-check-circle"></i></div>
                  <div className="text-[10px] font-bold text-gray-800 mt-2">AI संदेश</div>
                  <div className="text-[10px] text-gray-800 mt-2 line-clamp-3 text-left leading-tight bg-[#b8c494] p-1.5 rounded border border-[#a8b484]">
                    {messages[selectedMsg].display}
                  </div>
                  {isSpeaking && <div className="text-[8px] text-gray-700 mt-2 font-bold animate-pulse">🔊 Playing...</div>}
                </div>
              ) : null
            }
          </div>

          <div className="absolute bottom-1 w-full px-2 flex justify-between text-[8px] font-bold text-gray-700 z-10">
            <div>{currentView === 'reading' ? 'Back' : 'Menu'}</div>
            <div>Contacts</div>
          </div>
        </div>

        <div className="keypad mt-4">
          <div className="flex justify-center gap-4 mb-3">
            <button className="nav-btn bg-gray-700 text-white w-10 h-6 rounded"><i className="fas fa-minus"></i></button>
            <div className="relative w-16 h-16 bg-gray-800 rounded-full flex items-center justify-center border-2 border-gray-900 shadow-inner">
              <div className="absolute top-1 text-[8px] text-gray-400"><i className="fas fa-chevron-up"></i></div>
              <div className="absolute bottom-1 text-[8px] text-gray-400"><i className="fas fa-chevron-down"></i></div>
              <button className="w-6 h-6 rounded-full bg-gray-700 text-white flex items-center justify-center shadow"><i className="fas fa-check text-[10px]"></i></button>
            </div>
            <button onClick={() => navigate('back')} className="nav-btn bg-gray-700 text-white w-10 h-6 rounded"><i className="fas fa-minus"></i></button>
          </div>

          <div className="flex justify-between mb-3 gap-2">
            <button className="w-full bg-green-600 rounded py-1.5 text-white shadow"><i className="fas fa-phone-alt text-[10px]"></i></button>
            <button onClick={() => navigate('back')} className="w-full bg-red-500 rounded py-1.5 text-white shadow"><i className="fas fa-phone-slash text-[10px]"></i></button>
          </div>

          <div className="grid grid-cols-3 gap-x-3 gap-y-2 text-center text-white">
            <button className="num-key bg-gray-800 py-1.5 rounded shadow">1</button>
            <button className="num-key bg-gray-800 py-1.5 rounded shadow">2<br/><span className="text-[6px] text-gray-400">ABC</span></button>
            <button className="num-key bg-gray-800 py-1.5 rounded shadow">3<br/><span className="text-[6px] text-gray-400">DEF</span></button>
            <button className="num-key bg-gray-800 py-1.5 rounded shadow">4<br/><span className="text-[6px] text-gray-400">GHI</span></button>
            <button className="num-key bg-gray-800 py-1.5 rounded shadow">5<br/><span className="text-[6px] text-gray-400">JKL</span></button>
            <button className="num-key bg-gray-800 py-1.5 rounded shadow">6<br/><span className="text-[6px] text-gray-400">MNO</span></button>
            <button className="num-key bg-gray-800 py-1.5 rounded shadow">7<br/><span className="text-[6px] text-gray-400">PQRS</span></button>
            <button className="num-key bg-gray-800 py-1.5 rounded shadow">8<br/><span className="text-[6px] text-gray-400">TUV</span></button>
            <button className="num-key bg-gray-800 py-1.5 rounded shadow">9<br/><span className="text-[6px] text-gray-400">WXYZ</span></button>
            <button className="num-key bg-gray-800 py-1.5 rounded shadow">*</button>
            <button className="num-key bg-gray-800 py-1.5 rounded shadow">0</button>
            <button className="num-key bg-gray-800 py-1.5 rounded shadow">#</button>
          </div>

          <button onClick={handleVoiceAI} disabled={isRecording} className={`w-full mt-4 py-3 rounded-lg text-white font-bold text-sm shadow flex items-center justify-center gap-2 transition-all ${isRecording ? 'bg-red-600 animate-pulse' : 'bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 active:scale-95'}`}>
            {isRecording ? <><i className="fas fa-stop-circle"></i> Listening...  </> : <><i className="fas fa-microphone"></i> VOICE AI  </>}
          </button>
        </div>
      </div>
    </div>
  );
}
