import os 

print("✉️ Configurando email...")
email = "20241pvai0030008@estudantes.ifpr.edu.br"
comando = f"git config user.email \"{email}\""
os.system(comando)

print("🆕 Adicionando modificações...")
comando1 = "git add *"
os.system(comando1)

mensagem = input("🔤 Mensagem do commit: ")

while( len(mensagem) < 5 ):
    print("⚠️ Mensagem muito pequena, detalhe mais...")
    mensagem = input("🔤 Mensagem do commit: ")

print("✅ Registrando alterações...")
comando2 = f"git commit -m \"{mensagem}\" "
os.system(comando2)

print("🛜 Enviando projeto ao GitHub")
comando3 = "git push"
os.system(comando3)