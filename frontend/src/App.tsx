import { useState, useEffect } from "react";
import { createSession, generateFAQ } from "./api";

export default function App() {
  const [session, setSession] = useState<any>(null);
  const [faq, setFaq] = useState<string | null>(null);
  const [isConnecting, setIsConnecting] = useState(false);
  const [connectionError, setConnectionError] = useState<string | null>(null);

  useEffect(() => {
    document.title = "HelloSonar AI";
  }, []);

  const startSession = async () => {
    try {
      setIsConnecting(true);
      setConnectionError(null);
      const data = await createSession("mycompany");
      setSession(data);
    } catch (error) {
      setConnectionError("Failed to create session. Please try again.");
      console.error("Session creation error:", error);
    } finally {
      setIsConnecting(false);
    }
  };

  const finishSession = async () => {
    try {
      // DEMO: In real use, you'd get a real transcript from backend storage
      const demoTranscript = `
      العميل: ازيك؟
      المساعد: تمام الحمد لله، تحب تسأل عن ايه؟
      العميل: عايز اعرف سياسة الاسترجاع.
      المساعد: سياسة الاسترجاع بتقول كذا...
      `;
      const result = await generateFAQ(demoTranscript);
      setFaq(result.faq);
    } catch (error) {
      setConnectionError("Failed to generate FAQ. Please try again.");
      console.error("FAQ generation error:", error);
    }
  };

  return (
    <main className="p-8 space-y-4">
      <h1 style={{ fontSize: '2.2rem', fontWeight: 700, color: '#0369a1', marginBottom: 8, textAlign: 'center', letterSpacing: '0.02em' }}>
        HelloSonar AI
      </h1>
      <h2 style={{ fontSize: '1.2rem', fontWeight: 500, color: '#0ea5e9', marginBottom: 20, textAlign: 'center' }}>
        This is the voice agent that is going to help us write the documentation together
      </h2>
      <div style={{ textAlign: 'center', marginBottom: 24, color: '#0369a1', fontSize: '1.1rem' }}>
        👋 Welcome! Start a voice session to begin collaborating on your documentation.
      </div>

      {connectionError && (
        <div style={{ 
          background: '#fef2f2', 
          color: '#dc2626', 
          padding: '12px', 
          borderRadius: '8px', 
          textAlign: 'center',
          marginBottom: '16px'
        }}>
          {connectionError}
        </div>
      )}

      {!session && (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '200px' }}>
          <button 
            onClick={startSession} 
            disabled={isConnecting}
            style={{
              background: isConnecting ? '#9ca3af' : '#38bdf8',
              color: '#fff',
              border: 'none',
              borderRadius: '8px',
              padding: '12px 24px',
              fontSize: '1rem',
              fontWeight: '600',
              cursor: isConnecting ? 'not-allowed' : 'pointer',
              transition: 'background 0.2s'
            }}
          >
            {isConnecting ? 'Creating Session...' : 'Start Voice Session'}
          </button>
        </div>
      )}

      {session && (
        <div style={{ 
          background: '#fff', 
          border: '2px solid #38bdf8', 
          borderRadius: '12px',
          padding: '20px',
          marginTop: '20px'
        }}>
          <div style={{ minHeight: '200px', border: '2px dashed #38bdf8', borderRadius: '8px', padding: '20px' }}>
            {/* LiveKitRoom component would go here in production */}
            <div style={{ textAlign: 'center', padding: '20px' }}>
              <p style={{ fontSize: '1.1rem', color: '#0369a1', marginBottom: '16px' }}>
                ✅ Agent is running — speak now!
              </p>
              <p style={{ fontSize: '0.9rem', color: '#64748b', marginBottom: '8px' }}>
                Room: {session.room_name}
              </p>
              <button
                onClick={finishSession}
                style={{
                  background: '#10b981',
                  color: '#fff',
                  border: 'none',
                  borderRadius: '8px',
                  padding: '12px 24px',
                  fontSize: '1rem',
                  fontWeight: '600',
                  cursor: 'pointer',
                  transition: 'background 0.2s'
                }}
              >
                Finish & Generate FAQ
              </button>
            </div>
          </div>
          
          {faq && (
            <div style={{ marginTop: '20px' }}>
              <h3 style={{ color: '#0369a1', marginBottom: '12px' }}>Generated FAQ:</h3>
              <pre style={{ 
                background: '#f0f9ff', 
                color: '#0369a1', 
                borderRadius: '8px', 
                padding: '16px', 
                fontSize: '1rem', 
                overflowX: 'auto',
                whiteSpace: 'pre-wrap'
              }}>
                {faq}
              </pre>
            </div>
          )}
        </div>
      )}
    </main>
  );
}
