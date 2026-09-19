from pathlib import Path
p=Path('/home/ubuntu/learnflow-ai/client/src/pages/Home.tsx')
s=p.read_text()
start=s.index('function LoginGate({ onLogin }: { onLogin: () => void }) {')
end=s.index('function UsageLimitOverlay', start)
new='''function LoginGate({ onLogin }: { onLogin: () => void }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [stage, setStage] = useState<"email" | "password">("email");
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const continueWithEmail = () => {
    if (!email.trim() || !/^\\S+@\\S+\\.\\S+$/.test(email)) {
      setError("Enter a valid email address to continue.");
      return;
    }
    setError("");
    setNotice(`Email ready · set or enter the password for ${email.trim()}`);
    setStage("password");
  };
  const signInWithPassword = () => {
    if (password.length < 6) {
      setError("Password must be at least 6 characters.");
      return;
    }
    window.localStorage.setItem("learnflow-demo-email", email.trim());
    window.localStorage.setItem("learnflow-demo-password-set", "true");
    setError("");
    onLogin();
  };
  return <div className="login-gate"><div className="login-gate-glow" /><div className="login-gate-card"><div className="auth-brand"><LearnFlowMark /><span><strong>LearnFlow</strong><small>AI learning cockpit</small></span></div><div className="eyebrow">PERSONAL LEARNING WORKSPACE</div><h1>Learn smarter.<br /><em>Go further.</em></h1><p>Sign in to continue your conversations, quizzes, progress, and private learning memory.</p>{stage === "email" ? <><label className="login-field-label">Email address</label><input className="login-email" type="email" value={email} onChange={(event) => { setEmail(event.target.value); setError(""); }} onKeyDown={(event) => { if (event.key === "Enter") continueWithEmail(); }} placeholder="you@example.com" autoComplete="email" /><button className="primary-button full" onClick={continueWithEmail}><LogIn size={16} /> Continue with email</button></> : <><button className="auth-back" onClick={() => { setStage("email"); setError(""); }}><ChevronRight size={14} className="rotate-180" /> Change email</button><label className="login-field-label">Password</label><input className="login-email" type="password" value={password} onChange={(event) => { setPassword(event.target.value); setError(""); }} onKeyDown={(event) => { if (event.key === "Enter") signInWithPassword(); }} placeholder="Enter your password" autoComplete="current-password" /><small className="login-note password-note">Your password stays private to your workspace and is never shown in chat.</small><button className="primary-button full" onClick={signInWithPassword}><Lock size={16} /> Sign in securely</button></>}{notice && <small className="login-success">{notice}</small>}{error && <small className="login-error">{error}</small>}<div className="login-divider"><span>or</span></div><button className="oauth-button" onClick={onLogin}><span className="google-mark">G</span> Connect with Google</button><button className="ghost-button full login-create" onClick={onLogin}><Plus size={15} /> Create a new account</button><small className="login-note">Your learning data stays private to your workspace.</small></div></div>;
}
'''
s=s[:start]+new+s[end:]
p.write_text(s)
