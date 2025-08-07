# 🌐 Enderline

- [Discord Server](https://discord.gg/3Ggh5rT8uK)
- [Portfolio](https://enderline.netlify.app/)

---

## 🇧🇷 Guia: Como Usar o Discord Bot Essentials

### 📌 O que é o Discord Bot Essentials?

O **Discord Bot Essentials** é um bot pronto criado para ajudar desenvolvedores e donos de servidores a gerenciar:

- Sistema de economia  
- Loja de cargos  
- Recompensas diárias  
- Promoções  
- Rankings  

Ideal para comunidades que querem mais interatividade e recompensas. Mais funcionalidades serão adicionadas com as próximas atualizações.

---

### 🛠️ Como configurar o bot

1. **Abra o arquivo `main.py`**  
   Use qualquer editor de texto (VS Code, Sublime Text, Notepad++, ou até o Bloco de Notas).

2. **Edite as configurações importantes:**

   - Encontre a linha:
     ```python
     GUILD_ID = SERVER_ID
     ```
     Substitua `SERVER_ID` pelo ID do seu servidor no Discord:
     ```python
     GUILD_ID = 123456789012345678
     ```

   - Encontre a linha:
     ```python
     OWNER_ID = ID
     ```
     Substitua `ID` pelo seu ID de usuário no Discord:
     ```python
     OWNER_ID = 987654321098765432
     ```

---

### 🎁 Lootboxes e Promo Codes

- **Adicionar recompensas à lootbox:**
  ```python
  LOOT_REWARDS = [
      {"type": "coins", "amount": 300, "chance": 40},
      {"type": "coins", "amount": 1000, "chance": 10},
      {"type": "xp", "amount": 50, "chance": 30},
      {"type": "xp", "amount": 150, "chance": 10},
      {"type": "role", "role_name": "LootBox Winner", "duration_minutes": 60, "chance": 10}
  ]
  ```

- **Criar novos códigos promocionais:**
  ```python
  PROMO_CODES = {
      "BOASVINDAS": {"coins": 1500, "xp": 500},
      "NATAL2025": {"coins": 2500, "xp": 1000}
  }
  ```

---

### 🏪 Loja de Cargos

Para adicionar cargos à loja:

```python
LOJA_DE_CARGOS = {
    "✨：Vip": 11500,
    "👑：Elite": 25000,
}
```

> ⚠️ O nome do cargo deve ser **exatamente igual** ao nome existente no servidor do Discord.

---

### 🚀 Como iniciar o bot com o Homebrew

1. **Abra o terminal do Homebrew** após configurar o `main.py`.

2. **Digite `1` no teclado**  
   Isso abrirá a opção de inserir o token do bot.

3. **Cole o Token do seu Bot do Discord**  
   Vá até o [Discord Developer Portal](https://discord.com/developers/applications), copie o token e cole no terminal.  
   > ⚠️ **NUNCA compartilhe esse token com ninguém!**

4. **Digite `2` para iniciar o bot**  
   O bot estará online no seu servidor.

5. **Para desligar o bot corretamente:**  
   Pressione `CTRL + C` no terminal e feche a janela.

---

## 🇺🇸 Guide: How to Use Discord Bot Essentials

### 📌 What is Discord Bot Essentials?

**Discord Bot Essentials** is a ready-to-use bot designed to help developers and server owners manage:

- Economy system  
- Role shop  
- Daily rewards  
- Promotions  
- Leaderboards  

Perfect for communities that want to offer interactivity and rewards. More features will be added over time.

---

### 🛠️ How to configure the bot

1. **Open the file `main.py`**  
   Use any text editor (VS Code, Sublime Text, Notepad++, etc).

2. **Edit the key settings:**

   - Find this line:
     ```python
     GUILD_ID = SERVER_ID
     ```
     Replace `SERVER_ID` with your server’s ID:
     ```python
     GUILD_ID = 123456789012345678
     ```

   - Find this line:
     ```python
     OWNER_ID = ID
     ```
     Replace `ID` with your user ID:
     ```python
     OWNER_ID = 987654321098765432
     ```

---

### 🎁 Lootboxes and Promo Codes

- **Add lootbox rewards:**
  ```python
  LOOT_REWARDS = [
      {"type": "coins", "amount": 300, "chance": 40},
      {"type": "coins", "amount": 1000, "chance": 10},
      {"type": "xp", "amount": 50, "chance": 30},
      {"type": "xp", "amount": 150, "chance": 10},
      {"type": "role", "role_name": "LootBox Winner", "duration_minutes": 60, "chance": 10}
  ]
  ```

- **Create promo codes:**
  ```python
  PROMO_CODES = {
      "BOASVINDAS": {"coins": 1500, "xp": 500},
      "NATAL2025": {"coins": 2500, "xp": 1000}
  }
  ```

---

### 🏪 Role Shop

To add roles to the shop:

```python
LOJA_DE_CARGOS = {
    "✨：Vip": 11500,
    "👑：Elite": 25000,
}
```

> ⚠️ Role names must **exactly match** the names of roles on your server.

---

### 🚀 How to start the bot with Homebrew

1. **Open the Homebrew terminal** after configuring `main.py`.

2. **Press `1`** to insert your bot token.

3. **Paste your Discord Bot Token**  
   Go to the [Discord Developer Portal](https://discord.com/developers/applications), copy the token and paste it into Homebrew.  
   > ⚠️ **NEVER share this token with anyone!**

4. **Press `2` to start the bot**  
   Your bot will be online on your server.

5. **To shut down the bot properly:**  
   Press `CTRL + C` in the terminal and close the window.
