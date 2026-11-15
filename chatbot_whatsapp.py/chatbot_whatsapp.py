from flask import Flask, request, jsonify
import requests, time, random, os
app = Flask(__name__)
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "cayolins92")
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN", "")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID", "1369503676254268")
API_URL = f"https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/messages"
JA = set()
def enviar(para, texto):
    h = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
    p = {"messaging_product": "whatsapp", "to": para, "type": "text", "text": {"body": texto}}
    try:
        requests.post(API_URL, headers=h, json=p, timeout=10)
    except Exception as e:
        print(e)
def responder(t0):
    t = t0.lower().strip()
    if t in ["oi","ola","opa","eai","e ai","fala","bom dia","boa tarde","boa noite"]:
        return "Falaa, tudo bem? Aqui e o Cayo, beleza? Pode mandar sua duvida ai que eu te ajudo na hora. Se for pra pesquisar alguma coisa, me fala o que voce quer saber que eu ja procuro pra voce."
    if "pesquis" in t or "procur" in t or "preco" in t or "quanto custa" in t:
        return "Boa, posso procurar isso pra voce. Me fala direitinho o que voce quer saber? E preco, noticia, como faz alguma coisa? Quanto mais detalhe, melhor eu acho pra voce."
    if "ajuda" in t or "duvida" in t or "como faz" in t or "como funciona" in t:
        return "Pode mandar, que duvida e? Pode falar do seu jeito mesmo, sem formalidade. Se precisar pesquisar na internet eu pesquiso na hora pra voce."
    if "valeu" in t or "obrigado" in t or "obrigada" in t or "top" in t:
        return "Que isso, tamo junto! Se precisar de mais alguma coisa e so chamar. To por aqui."
    if "tchau" in t or "falou" in t or "fui" in t:
        return "Falouu, se cuida! Qualquer coisa chama aqui que eu respondo."
    return f"Boa, entendi. Voce quer saber sobre: {t0}. Me fala um pouquinho mais que eu ja te explico / procuro certinho pra voce."
@app.route("/webhook", methods=["GET"])
def verificar():
    mode = request.args.get("hub.mode"); tk = request.args.get("hub.verify_token"); ch = request.args.get("hub.challenge")
    if mode == "subscribe" and tk == VERIFY_TOKEN:
        return ch, 200
    return "Token invalido", 403
@app.route("/webhook", methods=["POST"])
def receber():
    data = request.get_json()
    try:
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                if "messages" not in value:
                    continue
                for msg in value.get("messages", []):
                    mid = msg.get("id")
                    if mid in JA:
                        continue
                    JA.add(mid)
                    if "group_id" in msg or "participant" in msg:
                        continue
                    if msg.get("type") != "text":
                        continue
                    remetente = msg.get("from"); texto = msg.get("text", {}).get("body", "")
                    if not remetente or not texto:
                        continue
                    time.sleep(random.uniform(0.8, 1.8))
                    enviar(remetente, responder(texto))
    except Exception as e:
        print(e)
    return jsonify({"status": "ok"}), 200
@app.route("/", methods=["GET"])
def home():
    return "Bot do Cayo rodando 24h - so privado, sem grupo", 200
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
