import tkinter as tk
from tkinter import ttk, scrolledtext
import random
import time
import threading

class CyberDefenseSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("🛡️ Advanced Cyber Defense Simulator v2.0")
        self.root.geometry("900x700")
        self.root.configure(bg="#0a0a0a")
        self.root.resizable(True, True)
        
        self.setup_ui()
        self.reset_game_state()
        
    def setup_ui(self):
        # Title
        title_frame = tk.Frame(self.root, bg="#0a0a0a")
        title_frame.pack(pady=10)
        
        title = tk.Label(title_frame, text="🛡️ CYBER DEFENSE SIMULATOR v2.0", 
                        font=("Orbitron", 20, "bold"), fg="#00ff88", bg="#0a0a0a")
        title.pack()
        
        subtitle = tk.Label(title_frame, text="Protect your assets from advanced cyber threats", 
                           font=("Consolas", 10), fg="#888888", bg="#0a0a0a")
        subtitle.pack(pady=(0, 10))
        
        # Control Panel
        control_frame = tk.Frame(self.root, bg="#1a1a1a", relief="raised", bd=2)
        control_frame.pack(pady=10, padx=20, fill="x")
        
        # Difficulty
        tk.Label(control_frame, text="Difficulty:", font=("Consolas", 10, "bold"), 
                fg="#00ff88", bg="#1a1a1a").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.level_var = tk.StringVar(value="medium")
        levels = [("🟢 Easy", "easy"), ("🟡 Medium", "medium"), ("🔴 Hard", "hard"), ("⚫ Expert", "expert")]
        self.level_menu = ttk.Combobox(control_frame, textvariable=self.level_var, 
                                      values=[name for name, val in levels], state="readonly",
                                      font=("Consolas", 10))
        self.level_menu.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        # Budget Slider
        tk.Label(control_frame, text="Defense Budget:", font=("Consolas", 10, "bold"), 
                fg="#00ff88", bg="#1a1a1a").grid(row=0, column=2, padx=10, pady=10, sticky="w")
        self.budget_var = tk.IntVar(value=50000)
        budget_scale = tk.Scale(control_frame, from_=10000, to=200000, orient="horizontal",
                               variable=self.budget_var, bg="#1a1a1a", fg="#00ff88",
                               highlightbackground="#1a1a1a", troughcolor="#333333")
        budget_scale.grid(row=0, column=3, padx=10, pady=10, sticky="ew")
        budget_label = tk.Label(control_frame, text="$50,000", font=("Consolas", 10),
                               fg="#00ff88", bg="#1a1a1a")
        budget_label.grid(row=0, column=4, padx=5)
        budget_scale.config(command=lambda v: budget_label.config(text=f"${int(float(v)):,}"))
        
        control_frame.columnconfigure(3, weight=1)
        
        # Stats Frame
        self.stats_frame = tk.Frame(self.root, bg="#1a1a1a", relief="raised", bd=2)
        self.stats_frame.pack(pady=10, padx=20, fill="x")
        
        self.score_labels = {}
        stats = ["💰 Total Loss", "🏦 Bank Score", "💻 Hacker Score", "🛡️ Security Level", "⚡ Budget Left"]
        for i, stat in enumerate(stats):
            label = tk.Label(self.stats_frame, text=f"{stat}: 0", font=("Consolas", 11, "bold"),
                           fg="#00ff88", bg="#1a1a1a")
            label.grid(row=0, column=i, padx=15, pady=10, sticky="ew")
            self.score_labels[stat] = label
        
        # Output Console
        console_frame = tk.Frame(self.root, bg="#0a0a0a")
        console_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        tk.Label(console_frame, text="📊 Attack Log", font=("Consolas", 12, "bold"),
                fg="#00ff88", bg="#0a0a0a").pack(anchor="w")
        
        self.output = scrolledtext.ScrolledText(console_frame, height=15, width=100,
                                              bg="#0d1117", fg="#00ff88", font=("Consolas", 10),
                                              insertbackground="#00ff88", selectbackground="#333333")
        self.output.pack(pady=5, fill="both", expand=True)
        
        # Control Buttons
        btn_frame = tk.Frame(self.root, bg="#0a0a0a")
        btn_frame.pack(pady=20)
        
        self.start_btn = tk.Button(btn_frame, text="▶ START SIMULATION", command=self.start_sim_thread,
                                  bg="#00ff88", fg="black", font=("Consolas", 12, "bold"),
                                  relief="raised", bd=3, padx=20, pady=5, cursor="hand2")
        self.start_btn.pack(side="left", padx=10)
        
        self.pause_btn = tk.Button(btn_frame, text="⏸ PAUSE", command=self.pause_simulation,
                                  bg="#ffaa00", fg="black", font=("Consolas", 11, "bold"),
                                  relief="raised", bd=3, padx=20, pady=5, cursor="hand2", state="disabled")
        self.pause_btn.pack(side="left", padx=10)
        
        self.reset_btn = tk.Button(btn_frame, text="🔄 RESET", command=self.reset_game,
                                  bg="#ff4444", fg="white", font=("Consolas", 11, "bold"),
                                  relief="raised", bd=3, padx=20, pady=5, cursor="hand2")
        self.reset_btn.pack(side="left", padx=10)
        
    def reset_game_state(self):
        self.is_running = False
        self.is_paused = False
        self.total_loss = 0
        self.bank_score = 0
        self.hacker_score = 0
        self.security_level = 50
        self.budget_left = 50000
        self.update_stats()
        
    def update_stats(self):
        self.score_labels["💰 Total Loss"].config(text=f"💰 Total Loss: ${self.total_loss:,.0f}")
        self.score_labels["🏦 Bank Score"].config(text=f"🏦 Bank Score: {self.bank_score}")
        self.score_labels["💻 Hacker Score"].config(text=f"💻 Hacker Score: {self.hacker_score}")
        self.score_labels["🛡️ Security Level"].config(text=f"🛡️ Security Level: {self.security_level}")
        self.score_labels["⚡ Budget Left"].config(text=f"⚡ Budget Left: ${self.budget_left:,}")
        
    def get_attacker_skill(self):
        level_map = {"easy": 40, "medium": 65, "hard": 85, "expert": 95}
        return level_map.get(self.level_var.get(), 65)
    
    def get_assets(self):
        return [
            {"name": "💳 Payment Gateway", "security": 75, "exposure": 55, "value": 150000, "critical": True},
            {"name": "🗄️ Customer Database", "security": 85, "exposure": 35, "value": 300000, "critical": True},
            {"name": "☁️ Cloud Storage", "security": 70, "exposure": 65, "value": 80000, "critical": False},
            {"name": "🔐 Authentication Server", "security": 90, "exposure": 25, "value": 120000, "critical": True},
            {"name": "📡 API Gateway", "security": 65, "exposure": 70, "value": 50000, "critical": False}
        ]
    
    def log(self, message):
        self.output.insert(tk.END, message + "\n")
        self.output.see(tk.END)
        self.root.update_idletasks()
    
    def start_sim_thread(self):
        if not self.is_running:
            self.reset_game_state()
            self.is_running = True
            self.start_btn.config(state="disabled")
            self.pause_btn.config(state="normal")
            thread = threading.Thread(target=self.run_simulation, daemon=True)
            thread.start()
    
    def pause_simulation(self):
        self.is_paused = not self.is_paused
        self.pause_btn.config(text="▶ RESUME" if self.is_paused else "⏸ PAUSE")
    
    def reset_game(self):
        self.is_running = False
        self.is_paused = False
        self.reset_game_state()
        self.output.delete(1.0, tk.END)
        self.start_btn.config(state="normal")
        self.pause_btn.config(state="disabled")
        self.pause_btn.config(text="⏸ PAUSE")
    
    def calculate_damage(self, attack_type, asset_value, critical=False):
        multipliers = {
            "DDoS": 0.15,
            "Ransomware": 0.35,
            "SQL Injection": 0.25,
            "Zero-Day": 0.45,
            "Phishing": 0.20,
            "MBR": 0.40
        }
        base_damage = asset_value * multipliers.get(attack_type, 0.2)
        return base_damage * (1.5 if critical else 1.0)
    
    def run_simulation(self):
        level = self.level_var.get()
        attacker_skill = self.get_attacker_skill()
        budget = self.budget_var.get()
        self.budget_left = budget
        
        self.log(f"🚀 SIMULATION STARTED - {level.upper()} MODE")
        self.log(f"🎯 Attacker Skill: {attacker_skill}% | 💰 Defense Budget: ${budget:,}")
        self.log(f"=" * 80)
        
        assets = self.get_assets()
        attack_types = ["DDoS", "Ransomware", "SQL Injection", "Zero-Day", "Phishing", "MBR"]
        
        for round_num in range(1, 11):  # 10 rounds for better gameplay
            if not self.is_running:
                break
                
            while self.is_paused:
                time.sleep(0.1)
                if not self.is_running:
                    return
            
            self.log(f"\n🔥 ROUND {round_num}/10 {'='*50}")
            
            round_bank = 0
            round_hacker = 0
            
            random.shuffle(assets)
            
            for asset in assets:
                if not self.is_running:
                    break
                    
                attack = random.choice(attack_types)
                
                # Enhanced probability calculation
                security_boost = min(self.budget_left * 0.0001, 20)  # Budget improves security
                current_security = asset["security"] + security_boost
                raw_prob = (asset["exposure"] + attacker_skill - current_security) / 100
                probability = max(0.05, min(0.95, raw_prob))  # Minimum 5% chance
                
                time.sleep(0.3)  # Dramatic pause
                
                if random.random() < probability:
                    damage = self.calculate_damage(attack, asset["value"], asset["critical"])
                    self.total_loss += damage
                    self.hacker_score += 15 if asset["critical"] else 10
                    round_hacker += 15 if asset["critical"] else 10
                    self.budget_left -= damage * 0.1  # Damage costs budget
                    
                    emoji = "💥" if asset["critical"] else "🔥"
                    self.log(f"  {emoji} [{asset['name']:<20}] {attack:<15} SUCCESS | "
                           f"💸 ${damage:,.0f} | 🔴 Sec: {current_security:.0f}%")
                else:
                    self.bank_score += 8 if asset["critical"] else 5
                    round_bank += 8 if asset["critical"] else 5
                    self.security_level += 2
                    self.log(f"  ✅ [{asset['name']:<20}] {attack:<15} BLOCKED  | "
                           f"🟢 Sec: {current_security:.0f}%")
                
                # Gradually improve security
                asset["security"] = min(95, asset["security"] + random.uniform(1, 4))
            
            self.log(f"📊 Round {round_num} → 🏦 {round_bank:3d} | 💻 {round_hacker:3d}")
            self.update_stats()
            
            # Check for early game over
            if self.hacker_score > self.bank_score + 50:
                self.log("\n💀 CRITICAL BREACH! SIMULATION TERMINATED.")
                break
        
        self.end_simulation()
    
    def end_simulation(self):
        self.is_running = False
        self.start_btn.config(state="normal")
        self.pause_btn.config(state="disabled")
        self.pause_btn.config(text="⏸ PAUSE")
        
        self.log(f"\n{'='*80}")
        self.log("🏁 SIMULATION COMPLETE")
        self.log(f"=" * 80)
        
        if self.total_loss > 250000 or self.hacker_score > self.bank_score:
            self.log("❌💻 HACKER VICTORY! Your systems have been compromised!")
            self.log("💡 Improve your security budget and asset protection.")
        else:
            self.log("✅🏦 BANK VICTORY! Your defenses held strong!")
            self.log("🎉 Excellent cybersecurity management!")
        
        self.log(f"\n📈 FINAL STATS:")
        self.log(f"   Total Loss:       ${self.total_loss:,.0f}")
        self.log(f"   Bank Score:       {self.bank_score}")
        self.log(f"   Hacker Score:     {self.hacker_score}")
        self.log(f"   Final Security:   {self.security_level:.0f}%")
        self.log(f"   Budget Remaining: ${self.budget_left:,.0f}")

def main():
    root = tk.Tk()
    app = CyberDefenseSimulator(root)
    root.mainloop()

if __name__ == "__main__":
    main()

