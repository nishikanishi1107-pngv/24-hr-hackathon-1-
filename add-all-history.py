from pathlib import Path
p = Path('/home/ubuntu/learnflow-ai/client/src/pages/Home.tsx')
s = p.read_text()
s = s.replace('useState<"active" | "archived">("active")', 'useState<"all" | "active" | "archived">("all")')
s = s.replace('historyFilter: "active" | "archived"; setHistoryFilter: (filter: "active" | "archived") => void;', 'historyFilter: "all" | "active" | "archived"; setHistoryFilter: (filter: "all" | "active" | "archived") => void;')
old = '<div className="history-tabs"><button className={historyFilter === "active" ? "active" : ""} onClick={() => setHistoryFilter("active")}>Chats <b>{history.filter((chat) => !chat.archived).length}</b></button><button className={historyFilter === "archived" ? "active" : ""} onClick={() => setHistoryFilter("archived")}>Archived <b>{history.filter((chat) => chat.archived).length}</b></button></div><div className="history-list">{history.filter((chat) => historyFilter === "archived" ? chat.archived : !chat.archived).map((chat) =>'
new = '<div className="history-tabs"><button className={historyFilter === "all" ? "active" : ""} onClick={() => setHistoryFilter("all")}>All History <b>{history.length}</b></button><button className={historyFilter === "active" ? "active" : ""} onClick={() => setHistoryFilter("active")}>Chats <b>{history.filter((chat) => !chat.archived).length}</b></button><button className={historyFilter === "archived" ? "active" : ""} onClick={() => setHistoryFilter("archived")}>Archived <b>{history.filter((chat) => chat.archived).length}</b></button></div><div className="history-list">{history.filter((chat) => historyFilter === "all" ? true : historyFilter === "archived" ? chat.archived : !chat.archived).map((chat) =>'
if old not in s:
    raise SystemExit('history UI anchor not found')
s = s.replace(old, new, 1)
p.write_text(s)
