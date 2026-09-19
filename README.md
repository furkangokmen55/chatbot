# Adaptive RAG Chatbot

LangChain + LangGraph ile kurulmuş, kendi kendini denetleyen (self-corrective) bir **RAG (Retrieval-Augmented Generation) chatbot**. PDF dokümanlarından oluşturulan bir vektör veritabanından cevap arar; bulduğu belgeler yetersiz veya konu dışıysa otomatik olarak web aramasına (Tavily) geçer, ürettiği cevabın hem kaynaklara dayandığını hem de soruyu gerçekten yanıtladığını kontrol eder.

## Mimari

Sistem bir **LangGraph state machine** olarak kurulu:

1. **Router** — Gelen soru, bir LLM tarafından değerlendirilip vektör veritabanına mı yoksa doğrudan web aramasına mı yönlendirileceğine karar verilir.
2. **Retrieve** — Soru, Chroma vektör veritabanından (PDF'lerden oluşturulmuş) ilgili belgeleri getirir.
3. **Grade Documents** — Getirilen her belge, soruyla alakalı olup olmadığına göre bir LLM ile puanlanır. Alakasız belge varsa web aramasına geçme bayrağı (`web_search`) set edilir.
4. **Web Search** (gerekirse) — Tavily arama API'siyle ek/alternatif kaynak bulunur.
5. **Generate** — Toplanan belgeler bağlam olarak kullanılıp LLM ile cevap üretilir.
6. **Hallucination Grader** — Üretilen cevabın, verilen belgelere gerçekten dayanıp dayanmadığı kontrol edilir; dayanmıyorsa cevap yeniden üretilir.
7. **Answer Grader** — Cevap, kullanıcının sorusunu gerçekten yanıtlıyor mu diye kontrol edilir; yanıtlamıyorsa web aramasına geri döner.

Bu akış, bilinen "Adaptive RAG / Corrective RAG / Self-RAG" desenlerinin bir kombinasyonu — hem yanlış/eksik belgeye karşı (corrective), hem de halüsinasyona karşı (self-RAG) koruma sağlıyor.

## Dosya Yapısı

| Dosya/Klasör | Açıklama |
|---|---|
| `ingestion.py` | `./pdfs` klasöründeki tüm PDF'leri okuyup parçalara ayırır (chunk), OpenAI embedding'leriyle Chroma vektör veritabanına yazar |
| `main.py` | Komut satırından etkileşimli sohbet döngüsü çalıştırır (Gradio arayüzü de kodda mevcut ama şu an yorum satırında/pasif) |
| `graph/graph.py` | LangGraph iş akışının tanımlandığı ana dosya — node'lar, koşullu geçişler ve karar fonksiyonları burada |
| `graph/nodes/` | `retrieve`, `grade_documents`, `generate`, `web_search` node fonksiyonları |
| `graph/chains/` | Router, retrieval grader, hallucination grader, answer grader gibi LLM zincirleri |
| `graph/state.py` | Graph'ın taşıdığı durumun (`question`, `generation`, `documents`, `web_search`) tanımı |
| `pdfs/` | Vektör veritabanına yüklenecek kaynak PDF dosyaları |
| `graph1.png`, `graph2.png`, `graph3.png` | LangGraph akışının görsel diyagramları (muhtemelen `draw_mermaid_png` ile üretilmiş) |
| `requirements.txt` | Python bağımlılıkları |

## Kurulum

```bash
pip install -r requirements.txt
```

Bir `.env` dosyası oluşturup gerekli API anahtarlarını ekle:
```
OPENAI_API_KEY=...
TAVILY_API_KEY=...
```

PDF dosyalarını `pdfs/` klasörüne koy, ardından vektör veritabanını oluştur:
```bash
python ingestion.py
```

Sohbeti başlat:
```bash
python main.py
```
Terminalde soru sorabilirsin; çıkmak için `çıkış` yaz.

## Not

`requirements.txt` içindeki `gradio==3.0.0` çok eski bir sürüm ve `main.py` içindeki Gradio arayüzü kodu şu an devre dışı (üç tırnak içinde yorum satırı) — sadece terminal tabanlı sohbet aktif durumda.
