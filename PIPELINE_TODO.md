# SafeMind Customer Pipeline — TODO

## Status: Waiting for email setup
## Created: 2026-05-13

---

## 1. Email Configuration (PENDING)

**Decision:** Create NEW email for SafeMind support.

**Action needed:** Arthur will create and share credentials.
- Preferred: `support@safemind.pro` or `safemind@yandex.ru`
- Once received → configure IMAP/SMTP in `~/.config/imap-smtp-email/.env`

---

## 2. Channel Priority

**Email = PRIMARY channel**
- Customer support inquiries
- Email newsletters/digests
- Official communications

**Telegram = SECONDARY channel**
- Quick chat via @Mentesegura_bot
- Community engagement
- Escalations from email

---

## 3. Response Autonomy — Escalation Plan

### Phase 1: Month 1 (Training)
**Process:**
1. Customer sends email
2. Kimicito drafts response (following SafeMind brand voice + contract terms)
3. Kimicito flags for Arthur review
4. Arthur approves/modifies
5. Kimicito sends

**Exception:** Simple FAQ (hours, pricing, how to join) — Kimicito can auto-respond with template

### Phase 2: After Arthur Approval
**Process:**
1. Customer sends email
2. Kimicito auto-responds within SLA (from pro.html contract)
3. Logs all interactions
4. Flags complex/escalation cases for Arthur

**Escalation triggers:**
- Refund requests
- Complaints about service quality
- Custom enterprise proposals
- Legal questions
- Anything outside SafeMind knowledge base

---

## 4. Pipeline Architecture (Draft)

```
Customer → Email/Telegram → [Unified Inbox]
                              ↓
                    [Kimicito triage]
                              ↓
            ┌──────────┬──────────┬──────────┐
            │ Auto-FAQ │  Draft   │ Escalate │
            │ (send)   │ → Arthur │ → Arthur │
            └──────────┴──────────┴──────────┘
```

---

## 5. Tools Needed

| Tool | Status | Purpose |
|------|--------|---------|
| IMAP/SMTP Email | ⏳ Waiting for credentials | Read/send support emails |
| Telegram Bot API | ✅ Ready | @Mentesegura_bot already configured |
| CRM/Database | ⏳ To be decided | Track customer interactions |
| Newsletter tool | ⏳ To be decided | Email digests/campaigns |

---

## 6. SLA Reference (from pro.html contract)

- Starter: ответы в течение 24 часов (пн-пт)
- Pro: ответы в течение 4 часов (пн-пт)
- Формат: текст + голосовые (Pro: + видеозвонок)
- Языки: русский, английский, испанский

---

## Next Steps

1. [ ] Arthur creates SafeMind support email
2. [ ] Configure IMAP/SMTP skill with credentials
3. [ ] Test: send test email → Kimicito reads → drafts response
4. [ ] Define FAQ templates (auto-response pool)
5. [ ] Set up cron/heartbeat for inbox monitoring
6. [ ] Document brand voice / response guidelines

---
*Return to this file when email is ready. Target: 2-3 days.*
