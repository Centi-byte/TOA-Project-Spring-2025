import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import networkx as nx

class PDA:
    def __init__(self, input_str):
        self.stack = ['z']
        self.input = input_str
        self.len = len(input_str)
        self.path = []
        self.accepted = self.q0(0)

    def q0(self, i):
        self.path.append(("q0", i, list(self.stack)))

        if i >= self.len:
            return False

        if self.input[i] == 'c':
            return self.q1(i + 1)

        if self.input[i] not in ['a', 'b']:
            return False

        self.stack.append(self.input[i])
        return self.q0(i + 1)

    def q1(self, i):
        self.path.append(("q1", i, list(self.stack)))

        if self.stack[-1] == 'z' and i >= self.len:
            return self.accept()

        if i >= self.len:
            return False

        if self.input[i] not in ['a', 'b']:
            return False

        if not self.stack or self.input[i] != self.stack[-1]:
            return False

        self.stack.pop()

        if self.stack[-1] == 'z' and i + 1 == self.len:
            return self.accept()

        return self.q1(i + 1)

    def accept(self): return True

#GUI features below

class PDAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDA Palindrome Checker")

        tk.Label(root, text="Enter string (use 'c' as middle marker):").pack()

        self.entry = tk.Entry(root, width=40)
        self.entry.pack()

        tk.Button(root, text="Check", command=self.run_pda).pack()
        tk.Button(root, text="Show State Diagram", command=self.draw_pda_graph).pack(pady=5)

        self.result_label = tk.Label(root, text="", font=("Arial", 14))
        self.result_label.pack(pady=10)

        self.stack_text = tk.Text(root, height=10, width=50)
        self.stack_text.pack()

    def run_pda(self):
        input_str = self.entry.get()
        pda = PDA(input_str)
        self.stack_text.delete('1.0', tk.END)

        if pda.accepted:
            self.result_label.config(text="Accepted", fg="green")
        else:
            self.result_label.config(text="Rejected", fg="red")

        for state, i, stack in pda.path:
            self.stack_text.insert(tk.END, f"State: {state}, Pos: {i}, Stack: {stack}\n")

    def draw_pda_graph(self):
        G = nx.MultiDiGraph()

        # Add states
        states = ["q0", "q1", "accept"]
        G.add_nodes_from(states)

        # Transitions
        G.add_edge("q0", "q0", label="a/b, push")
        G.add_edge("q0", "q1", label="c")
        G.add_edge("q1", "q1", label="a/b, pop")
        G.add_edge("q1", "accept", label="z")

        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10)
        edge_labels = {(u, v): d['label'] for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        plt.title("PDA State Diagram")
        plt.axis('off')
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = PDAApp(root)
    root.mainloop()
