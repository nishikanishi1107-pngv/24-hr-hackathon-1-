from pathlib import Path
p = Path('/home/ubuntu/learnflow-ai/client/src/pages/Home.tsx')
s = p.read_text()
s = s.replace('  const [credits, setCredits] = useState(1250);', '  const [credits, setCredits] = useState(1250);\n  const [dailyCredits, setDailyCredits] = useState(200);')
s = s.replace('  const [usageSeconds, setUsageSeconds] = useState(0);\n  const [usageLocked, setUsageLocked] = useState(false);\n  const [cooldownSeconds, setCooldownSeconds] = useState(0);', '  const [creditCooldownSeconds, setCreditCooldownSeconds] = useState(0);')
start = s.index('  useEffect(() => {\n    const savedUsage = Number(window.localStorage.getItem("learnflow-usage-seconds") || 0);')
end = s.index('  useEffect(() => {\n    if (!challengeActive', start)
new_effect = '''  useEffect(() => {
    const savedCredits = Number(window.localStorage.getItem("learnflow-daily-credits"));
    const savedCooldown = Number(window.localStorage.getItem("learnflow-credit-cooldown-until") || 0);
    if (Number.isFinite(savedCredits) && savedCredits >= 0 && savedCredits <= 200) setDailyCredits(savedCredits);
    if (savedCooldown > Date.now()) setCreditCooldownSeconds(Math.ceil((savedCooldown - Date.now()) / 1000));
  }, []);
  useEffect(() => {
    const timer = window.setInterval(() => {
      const cooldownUntil = Number(window.localStorage.getItem("learnflow-credit-cooldown-until") || 0);
      if (cooldownUntil > Date.now()) {
        setCreditCooldownSeconds(Math.ceil((cooldownUntil - Date.now()) / 1000));
        return;
      }
      if (cooldownUntil) {
        window.localStorage.removeItem("learnflow-credit-cooldown-until");
        window.localStorage.setItem("learnflow-daily-credits", "200");
        setDailyCredits(200);
        setCreditCooldownSeconds(0);
      }
    }, 1000);
    return () => window.clearInterval(timer);
  }, []);
'''
s = s[:start] + new_effect + s[end:]
start = s.index('  const sessionRemaining = Math.max(0, 7200 - usageSeconds);')
end = s.index('  const pushToast =', start)
s = s[:start] + '  const dailyCreditsLabel = `${dailyCredits} credits remaining`;\n' + s[end:]
old = '''    if (!content || typing) return;
    setChatInput("");'''
new = '''    if (!content || typing) return;
    if (creditCooldownSeconds > 0 || dailyCredits < 5) {
      pushToast(creditCooldownSeconds > 0 ? "Credits are resting · try again when the 1-hour reset ends" : "Daily credits finished · a fresh 200 credits arrive after 1 hour");
      return;
    }
    const nextDailyCredits = dailyCredits - 5;
    setDailyCredits(nextDailyCredits);
    window.localStorage.setItem("learnflow-daily-credits", String(nextDailyCredits));
    if (nextDailyCredits === 0) {
      const nextCooldown = Date.now() + 3600000;
      window.localStorage.setItem("learnflow-credit-cooldown-until", String(nextCooldown));
      setCreditCooldownSeconds(3600);
    }
    setChatInput("");'''
s = s.replace(old, new, 1)
old = '      setTyping(true);\n      chatMutation.mutate({'
new = '      setTyping(true);\n      chatMutation.mutate({'
# Reward when answer arrives, immediately after successful mutation callback is handled below.
s = s.replace('  const dailyCreditsLabel = `${dailyCredits} credits remaining`;', '  const dailyCreditsLabel = `${dailyCredits} credits remaining`;')
s = s.replace('sessionRemainingLabel={sessionRemainingLabel}', 'dailyCreditsLabel={dailyCreditsLabel}')
s = s.replace('  const submitChallenge = () => {', '  const submitChallenge = () => {')
s = s.replace('    setCredits((value) => value + (result === "correct" ? 10 : result === "partial" ? 5 : 0));', '    setCredits((value) => value + (result === "correct" ? 10 : result === "partial" ? 5 : 0));')
s = s.replace('challengeQuestion: string; sessionRemainingLabel: string;', 'challengeQuestion: string; dailyCreditsLabel: string;')
s = s.replace('<Clock3 size={12} /> {props.sessionRemainingLabel} of active learning time', '<Sparkles size={12} /> {props.dailyCreditsLabel} · 5 credits per AI answer')
s = s.replace('      {usageLocked && <UsageLimitOverlay cooldownSeconds={cooldownSeconds} />}\n', '')
# Award 5 total credits when the tutor returns an answer, once per response.
s = s.replace('    setTyping(false);\n    setExplanationText(reply.answer);', '    setTyping(false);\n    setCredits((value) => value + 5);\n    pushToast("+5 credits · Tutor answer completed");\n    setExplanationText(reply.answer);', 1)
p.write_text(s)
