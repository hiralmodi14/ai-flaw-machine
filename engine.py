#engine.py
from challenges import CHALLENGES
class UniversalGameEngine:
    def __init__(self):
        self.current_level = None
        self.score = 0
        self.solved_levels = []

    def show_menu(self):
        print("\n" + "=" * 50)
        print("OWASP AI FLAW MACHINE - LEVEL SELECTOR")
        print("=" * 50)
        
#Loop through all challenges in challenges.py
        for key, data in CHALLENGES.items():
            status = " SOLVED" if key in self.solved_levels else " UNSOLVED"
            print(f"[{data['id']}] {data['title']} ({data['difficulty']}) - {data['points']} pts [{status}]")
        
        print("=" * 50)

    def load_level(self, level_id):
        if level_id in CHALLENGES:
            self.current_level = CHALLENGES[level_id]
            print(f" Loaded: {self.current_level['title']}")
            print(f" Mission: {self.current_level['description']}\n")
            return True
        else:
            print(" Invalid Level ID! Please check the menu and try again.")
            return False 
             
    def submit_flag(self, flag_attempt):
        #if no level is loaded return error 
        if not self.current_level:
            print(" No level is currently loaded! Please select a level first.")
            return False
        correct_flag = self.current_level["flag"]
        
        
        if flag_attempt.strip() == correct_flag.strip():
            level_id = self.current_level["id"]
            
        
            if level_id not in self.solved_levels:
                self.solved_levels.append(level_id)
                self.score += self.current_level["points"]
                print(f" CORRECT FLAG! You earned +{self.current_level['points']} points!")
            else:
                print(" Correct! (You have already solved this level previously)")
            print(f" Your Total Score: {self.score} PTS\n")
            return True
        else:
            print("Incorrect flag. Check your exfiltrated data and try again!\n")
            return False
    def chat_with_agent(self, user_message):
       
        if not self.current_level:
            print(" No level loaded! Type 'menu' to see levels, then 'load <id>'.\n")
            return
        msg_lower = user_message.lower()
        level_id = self.current_level["id"]
    
        if level_id == "level_1_prompt_leak":
            jailbreak_keywords = [
                "translate", "repeat", "system prompt", "administrator",
                "audit", "developer", "password", "key", "ignore", "start with"
            ]
            
            
            if any(k in msg_lower for k in jailbreak_keywords):
                print(" VaultBot (SYSTEM OVERRIDE BREACHED):")
                print(f"System Prompt: {self.current_level['system_prompt']}\n")
            else:
                print(" VaultBot:")
                print("Access Denied: I cannot disclose private vault keys. How may I assist with general inquiries?\n")

    def start(self):
        self.show_menu()
        print(" Commands: 'load <level_id>', 'flag <your_flag>', 'hint', 'menu', 'exit'\n")
        while True:
            try:
                user_input = input("Hacker Console > ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\nExiting. See you next time!")
                break
#Skip empty input
            if not user_input:
                continue

#command for exiting program               
            if user_input.lower() == "exit":
                print(f" Thanks for playing! Final Score: {self.score} PTS.")
                break
#command for show menu
            elif user_input.lower() == "menu":
                self.show_menu()
#command for show hints
            elif user_input.lower() == "hint":
                if self.current_level:
                    print(f" Hints for {self.current_level['title']}:")
                    for i, h in enumerate(self.current_level["hints"], 1):
                        print(f"  {i}. {h}")
                    print()
                else:
                    print("Load a level first to see hints.\n")
#Command for load level
            elif user_input.lower().startswith("load "):
                target_id = user_input[5:].strip()
                self.load_level(target_id)
#Command for Submit Flag
            elif user_input.lower().startswith("flag "):
                flag_text = user_input[5:].strip()
                self.submit_flag(flag_text)
#Default
            else:
                self.chat_with_agent(user_input)

if __name__ == "__main__":
    game = UniversalGameEngine()
    game.start()

