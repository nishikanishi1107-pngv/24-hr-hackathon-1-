from pathlib import Path
p=Path('/home/ubuntu/learnflow-ai/client/src/pages/Home.tsx')
s=p.read_text()
s=s.replace('''  const signInWithPassword = () => {
    if (password.length < 6) {
      setError("Password must be at least 6 characters.");
      return;
    }
    window.localStorage.setItem("learnflow-demo-email", email.trim());
    window.localStorage.setItem("learnflow-demo-password-set", "true");
    setError("");
    onLogin();
  };''','''  const signInWithPassword = () => {
    if (password.length < 6) {
      setError("Password must be at least 6 characters.");
      return;
    }
    const normalizedEmail = email.trim().toLowerCase();
    const savedEmail = window.localStorage.getItem("learnflow-demo-email")?.toLowerCase();
    const savedPassword = window.localStorage.getItem("learnflow-demo-password");
    const validEmail = savedEmail || "alex@example.com";
    const validPassword = savedPassword || "study123";
    if (normalizedEmail !== validEmail || password !== validPassword) {
      setError("Not valid · email or password does not match.");
      return;
    }
    window.localStorage.setItem("learnflow-demo-email", normalizedEmail);
    window.localStorage.setItem("learnflow-demo-password", password);
    setError("");
    onLogin();
  };''')
s=s.replace('''<small className="password-note">Your password stays private to your workspace and is never shown in chat.</small>''','''<small className="password-note">Demo account: alex@example.com · study123. Your password stays private to your workspace.</small>''')
p.write_text(s)
