from pathlib import Path
p=Path('/home/ubuntu/learnflow-ai/client/src/pages/Home.tsx')
s=p.read_text()
s=s.replace('  const [offlineLoading, setOfflineLoading] = useState(false);', '  const [offlineLoading, setOfflineLoading] = useState(false);\n  const [offlineQuestionCount, setOfflineQuestionCount] = useState(0);')
s=s.replace('''    if (!question || offlineLoading) return;
    setOfflineLoading(true);''','''    if (!question || offlineLoading) return;
    if (offlineQuestionCount >= 2) {
      setOfflineAnswer("Offline session limit reached: you can ask only 2 questions during this session. Start a new session later to continue.");
      pushToast("Offline limit reached · 2 questions per session");
      return;
    }
    setOfflineQuestionCount((value) => value + 1);
    setOfflineLoading(true);''',1)
s=s.replace('''<div className="eyebrow">QUICK QUESTION</div><h3>What do you need to remember?</h3>''','''<div className="eyebrow">QUICK QUESTION · {Math.min(offlineQuestionCount, 2)} / 2 USED</div><h3>What do you need to remember?</h3>''',1)
s=s.replace('''<button className="primary-button" onClick={generate} disabled={loading || !query.trim()}><WifiOff size={16} /> {loading ? "Thinking..." : "Ask offline AI"}</button>''','''<button className="primary-button" onClick={generate} disabled={loading || !query.trim() || questionCount >= 2}><WifiOff size={16} /> {loading ? "Checking locally..." : questionCount >= 2 ? "2 questions used" : "Ask offline AI"}</button>''',1)
s=s.replace('function OfflineView({ query, setQuery, answer, generate, loading }: { query: string; setQuery: (value: string) => void; answer: string; generate: () => void; loading: boolean }) {', 'function OfflineView({ query, setQuery, answer, generate, loading, questionCount }: { query: string; setQuery: (value: string) => void; answer: string; generate: () => void; loading: boolean; questionCount: number }) {')
s=s.replace('loading={offlineLoading} />', 'loading={offlineLoading} questionCount={offlineQuestionCount} />')
p.write_text(s)
