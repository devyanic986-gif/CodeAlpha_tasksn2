import sys
import random
import typing
#Devyani Chaudhari
# Data: quotes

QUOTES = [
    ("THERE ARE NO SHORTCUTS TO ANY PLACE WORTH GOING.", "BEVERLY SILLS"),
    ("I think that whatever your journey takes you, there are new gods waiting there, with divine patience -and laughter.", "SUSAN M. WATKINS"),
    ("Nothing great was ever achieved without enthusiasm.", "RALPH WALDO EMERSON"),
    ("Life is what happens when you're busy making other plans.", "John Lennon"),
    ("The only limit to our realization of tomorrow is our doubts of today.", "Franklin D. Roosevelt"),
    ("In the middle of difficulty lies opportunity.", "Albert Einstein"),
    ("Your time is limited, so don't waste it living someone else's life.", "Steve Jobs"),
    ("Whether you think you can or you think you can't, you're right.", "Henry Ford"),
    ("It always seems impossible until it's done.", "Nelson Mandela"),
    ("Success is not final, failure is not fatal: it is the courage to continue that counts.", "Winston Churchill"),
    ("If you want to go fast, go alone. If you want to go far, go together.", "African Proverb"),
    ("Do what you can, with what you have, where you are.", "Theodore Roosevelt"),
    ("The best way to predict the future is to create it.", "Peter Drucker"),
    ("Happiness is not something ready-made. It comes from your own actions.", "Dalai Lama"),
    ("We are what we repeatedly do. Excellence, then, is not an act, but a habit.", "Will Durant"),
    ("Strive not to be a success, but rather to be of value.", "Albert Einstein"),
    ("It is never too be what you might have been.", "GEORGE ELIOT"),
    ("The heart of the wise man lies quiet like limpid water.", "CAMEROONIAN SAYING"),
    ("Dream big and dare to fail.", "Norman Vaughan"),
    ("If you can dream it, you can do it.", "Walt Disney"),
    ("Everything you have ever wanted is on the other side of fear.", "George Addair"),
    ("LESS IS MORE.", "ROBERT BROWNING"),
    ("One doesn't discover new lands without consenting to lose sight of the shore for a very long time.", "ANDRE GIDE"),
    ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
    ("The secret of getting ahead is getting started.", "Mark Twain"),
    ("The future depends on what you do today.", "Mahatma Gandhi"),
    ("Quality is not an act, it is a habit.", "Aristotle"),
    ("Kindness is more important than wisdom, and the recognition of this is the begining of wisdom.", "THEODORE ISAAC RUBIN"),
    ("ALWAYS BE A LITTEL KINDER THAN NECESSARY.", "SIR JAMES M. BARRIE"),
    ("..WE may measure our road to wisdom by the sorrows we have undergone.", "BULWER"),
    ("Too much sunshine makes a desert. In sorrow we discover the things which really matter; in sarrow we discover ourselves.", "ARAB PROVERB"),
    ("REMEMBER THIS - THAT VERY LITTLE IS NEEDED TO MAKE A HAPPY LIFE.", "MARCUS AURELIUS"),
]
# QuoteManager
class QuoteManager:
    
    def __init__(self, quotes: typing.List[typing.Tuple[str, str]], rng=None):
        self.quotes = list(quotes)
        self.last_index: typing.Optional[int] = None
        self.rng = rng if rng is not None else random

    def pick_quote_index(self) -> typing.Optional[int]:
        if not self.quotes:
            return None
        if len(self.quotes) == 1:
            return 0
        idx = self.rng.randrange(len(self.quotes))
        while self.last_index is not None and idx == self.last_index:
            idx = self.rng.randrange(len(self.quotes))
        return idx

    def get_quote(self) -> typing.Tuple[typing.Optional[str], typing.Optional[str]]:
        idx = self.pick_quote_index()
        if idx is None:
            return None, None
        self.last_index = idx
        q, a = self.quotes[idx]
        return q, a


def run_gui(manager: QuoteManager):
    try:
        import tkinter as tk
        from tkinter import messagebox
    except Exception as e:
        raise

    class QuoteApp(tk.Tk):
        def __init__(self, manager: QuoteManager):
            super().__init__()
            self.manager = manager
            self.title("Random Quote Generator")
            self.geometry("1020x720")
            self.minsize(500, 300)
            self.configure(bg="#0d0503")

            container = tk.Frame(self, bg="#16b3d3", padx=50, pady=50)
            container.pack(expand=True, fill="both")

            self.quote_text = tk.Label(
                container,
                text="",
                font=("sans sarif", 18, "normal"),
                wraplength=660,
                justify="center",
                fg="#111111",
                bg="#e7f308",
                padx=8,
                pady=8,
            )
            self.quote_text.pack(expand=True, fill="both")

            self.author_text = tk.Label(
                container,
                text="",
                font=("fancy script bold", 14, "italic"),
                fg="#555555",
                bg="#e50ee2",
                pady=8,
            )
            self.author_text.pack()

            btn_bar = tk.Frame(container, bg="#ffffff")
            btn_bar.pack(pady=8)

            self.new_btn = tk.Button(
                btn_bar,
                text="New Quote",
                command=self.show_new_quote,
                relief="groove",
                padx=16,
                pady=8,
            )
            self.new_btn.pack(side=tk.LEFT, padx=6)

            self.copy_btn = tk.Button(
                btn_bar,
                text="Copy",
                command=self.copy_to_clipboard,
                relief="groove",
                padx=16,
                pady=8,
            )
            self.copy_btn.pack(side=tk.LEFT, padx=6)

            self.bind("<space>", lambda e: self.show_new_quote())
            self.bind("<Return>", lambda e: self.show_new_quote())
            self.bind("<Control-c>", lambda e: self.copy_to_clipboard())

            self.show_new_quote()

        def show_new_quote(self):
            q, a = self.manager.get_quote()
            if q is None:
                self.quote_text.config(text="No quotes available.")
                self.author_text.config(text="")
                return
            self.quote_text.config(text=f"“{q}”")
            self.author_text.config(text=f"— {a}")

        def copy_to_clipboard(self):
            q = self.quote_text.cget("text").strip('“”')
            a = self.author_text.cget("text").replace("— ", "").strip()
            full = f'"{q}" — {a}' if q and a else q or a
            if full:
                try:
                    # tkinter clipboard
                    self.clipboard_clear()
                    self.clipboard_append(full)
                    self.update()
                    messagebox.showinfo("Copied", "Quote copied to clipboard!")
                except Exception:
                    messagebox.showwarning("Copy failed", "Could not copy to clipboard.")

    app = QuoteApp(manager)
    app.mainloop()
#fallback for environments without tkinter
def run_console(manager: QuoteManager):
    try:
        import pyperclip
        have_pyperclip = True
    except Exception:
        have_pyperclip = False

    def copy_text(text: str):
        if have_pyperclip:
            try:
                pyperclip.copy(text)
                print("(Copied to clipboard)")
            except Exception:
                print("(Failed to copy to clipboard)")
        else:
            print("(pyperclip not installed — install it to enable clipboard copy)" )

    print("Random Quote Generator — Console Mode")
    print("Press Enter for a new quote, 'c' then Enter to copy, 'q' then Enter to quit.")

    # Show first quote
    q, a = manager.get_quote()
    if q is None:
        print("No quotes available.")
        return
    while True:
        print('\n' + '“' + q + '”')
        print(f"— {a}")
        cmd = input('\nCommand [Enter=new, c=copy, q=quit]: ').strip().lower()
        if cmd == 'q':
            print('Goodbye!')
            break
        if cmd == 'c':
            copy_text(f'"{q}" — {a}')
            continue
        q, a = manager.get_quote()
        if q is None:
            print('No more quotes.')
            break

import unittest

class TestQuoteManager(unittest.TestCase):
    def test_empty_quotes(self):
        mgr = QuoteManager([], rng=random.Random(0))
        self.assertIsNone(mgr.pick_quote_index())
        self.assertEqual(mgr.get_quote(), (None, None))

    def test_single_quote(self):
        single = [("Only one", "Me")]
        mgr = QuoteManager(single, rng=random.Random(0))
        #always return 0
        for _ in range(5):
            self.assertEqual(mgr.pick_quote_index(), 0)
            q, a = mgr.get_quote()
            self.assertEqual((q, a), ("Only one", "Me"))

    def test_no_immediate_repeat(self):
        quotes = [(f'q{i}', f'a{i}') for i in range(5)]
        rng = random.Random(12345)
        mgr = QuoteManager(quotes, rng=rng)
        last = None
        for _ in range(100):
            idx = mgr.pick_quote_index()
    
            if last is not None and len(quotes) > 1:
                self.assertNotEqual(idx, last)
            last = idx
            mgr.last_index = idx

    def test_get_quote_updates_last_index(self):
        quotes = [("a","A"), ("b","B")]
        rng = random.Random(1)
        mgr = QuoteManager(quotes, rng=rng)
        q, a = mgr.get_quote()
        self.assertIn(q, {"a","b"})
        self.assertIn(a, {"A","B"})
        self.assertIsNotNone(mgr.last_index)

# Entry point
def main():
    manager = QuoteManager(QUOTES)
    #if tkinter not available, fall back to console
    try:
        run_gui(manager)
    except Exception as e:
        print("GUI unavailable (tkinter missing or failed to initialise). Falling back to console mode.")
        run_console(manager)


if __name__ == "__main__":
    main()

