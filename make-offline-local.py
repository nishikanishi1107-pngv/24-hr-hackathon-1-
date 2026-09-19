from pathlib import Path
p=Path('/home/ubuntu/learnflow-ai/client/src/pages/Home.tsx')
s=p.read_text()
s=s.replace('  const [offlineAnswer, setOfflineAnswer] = useState("");', '  const [offlineAnswer, setOfflineAnswer] = useState("");\n  const [offlineLoading, setOfflineLoading] = useState(false);')
old='''  const offlineChatMutation = trpc.ai.chat.useMutation({
    onSuccess: (data) => {
      setOfflineAnswer(capOfflineResponse(data.answer, 100));
    },
    onError: () => {
      setOfflineAnswer(capOfflineResponse("Offline mode could not reach the tutor right now. Please try again with a little more detail in your question.", 100));
    },
  });
  const generateOfflineAnswer = () => {
    const question = offlineQuery.trim();
    if (!question || offlineChatMutation.isPending) return;
    offlineChatMutation.mutate({
      topic: "offline quick answer",
      messages: [{ role: "user", content: question }],
    });
  };'''
new='''  const generateOfflineAnswer = () => {
    const question = offlineQuery.trim();
    if (!question || offlineLoading) return;
    setOfflineLoading(true);
    window.setTimeout(() => {
      const lower = question.toLowerCase();
      let answer = "Offline mode: I can explain the idea using the local study guide. Break the topic into its meaning, one small example, and a quick practice step.";
      if (/tamil|தமிழ்|tanglish|enna|epdi|na enna|meaning/.test(lower)) answer = "Offline answer: Indha concept-oda meaning-ai simple-a paathaa, idhu oru problem-ai small steps-aa split panni purinjukka help pannum. Oru small example try pannunga; apram answer-ai unga own words-la solli paarunga.";
      else if (/loop|for loop|while loop/.test(lower)) answer = "A loop repeats a block of code while a condition is true. A for loop is useful when you know the count; a while loop is useful when repetition depends on a condition. Always update the loop variable and include a stopping condition to avoid an infinite loop.";
      else if (/stack/.test(lower)) answer = "A stack stores items in last-in, first-out order. The last item pushed is the first item popped. Think of plates: push adds a plate, pop removes the top plate, and peek checks the top without removing it.";
      else if (/queue/.test(lower)) answer = "A queue stores items in first-in, first-out order. The first item added is the first item removed, like people waiting in a line. Enqueue adds at the back; dequeue removes from the front.";
      else if (/recursion|recursive/.test(lower)) answer = "Recursion is when a function calls itself on a smaller version of the problem. It needs a base case to stop and a recursive step that moves toward that base case. Without the base case, calls continue indefinitely.";
      else if (/array|list/.test(lower)) answer = "An array keeps multiple values in an ordered collection. Each value has an index, usually starting at zero. Use arrays for fast indexed access, and always check the index range before reading or writing a value.";
      else if (/velocity|speed|force|formula|math|calculate/.test(lower)) answer = "For a physics calculation, write the known values first, choose the matching formula, substitute the values with units, calculate carefully, and state the final unit. For example, velocity means displacement divided by time: v = d ÷ t.";
      else if (/project|idea|plan|certificate|coding/.test(lower)) answer = "Start with the goal, list the smallest useful features, choose the tools, and build one testable step first. Keep notes about risks, save versions regularly, and finish with a short demo or explanation of what you learned.";
      setOfflineAnswer(capOfflineResponse(answer, 100));
      setOfflineLoading(false);
    }, 180);
  };'''
if old not in s: raise SystemExit('offline mutation block not found')
s=s.replace(old,new,1)
s=s.replace('loading={offlineChatMutation.isPending}', 'loading={offlineLoading}')
s=s.replace('No internet required · maximum 100 words per explanation', 'No internet or API required · answers run on this device · maximum 100 words')
p.write_text(s)
