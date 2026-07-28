# DNS as it stood before the migration

Captured 28 July 2026, before anything was changed. If a step goes wrong, this
is what the zone looked like and what to restore.

## Registrar and nameservers

Registered at **Namecheap**. Nameservers:

```
dns1.registrar-servers.com
dns2.registrar-servers.com
```

## Records

| Type | Name | Value | Note |
|---|---|---|---|
| A | `yonatanshamam.com` | `206.81.21.82` | the live WordPress site on Cloudways |
| A | `www.yonatanshamam.com` | `206.81.21.82` | same host |
| MX | `yonatanshamam.com` | `eforward1.registrar-servers.com` | priority 10 |
| MX | `yonatanshamam.com` | `eforward2.registrar-servers.com` | priority 10 |
| MX | `yonatanshamam.com` | `eforward3.registrar-servers.com` | priority 10 |
| MX | `yonatanshamam.com` | `eforward4.registrar-servers.com` | priority 15 |
| MX | `yonatanshamam.com` | `eforward5.registrar-servers.com` | priority 20 |
| TXT | `yonatanshamam.com` | `v=spf1 include:spf.efwd.registrar-servers.com ~all` | SPF for the forwarding |

## What the MX records mean

**Namecheap email forwarding is already active on this domain.** There may
already be a working address. Before touching the nameservers, open the
Namecheap dashboard, list every forwarding rule, and write it down here —
those rules are not visible from outside and cannot be recovered from DNS.

## The trap in this migration

Namecheap's free email forwarding only runs while **their** nameservers are
authoritative. Pointing the domain at Cloudflare stops the forwarding even if
the MX records are copied across, because the service is tied to their DNS
rather than to the records alone.

So Cloudflare Email Routing has to be configured in the same session as the
nameserver change, not after it. Mail sent in the gap is bounced, not queued.

## The old site is gone — 28 July 2026

The founder deleted the Cloudways account, so `206.81.21.82` refuses
connections on both 80 and 443. Confirmed from two networks.

What that changes:

- **The two A records point at nothing.** Left proxied, Cloudflare answers 522
  instead of a connection error. Neither is good; both are temporary. They get
  replaced when the Worker is deployed.
- **Email is unaffected for now.** Forwarding runs through Namecheap, not
  Cloudways, so it keeps working until the nameservers move — at which point
  the trap described above applies exactly as written.
- **There is no longer a live site to protect**, so nothing in this migration
  carries risk to production. The caution below is kept for the record.
- **Deployment became the urgent item.** A domain answering errors starts
  losing whatever index position it has.

On that last point, the loss is smaller than it sounds. The research at the
start of this project found the old site had almost no organic presence:
searching `"יהונתן שמם" עורך דין` did not return it at all, and only one blog
post was indexed. There is very little to lose.

## Order that keeps the live site up

The A record is what keeps the current site reachable. Cloudflare imports it
during setup, so the live WordPress site keeps answering on `206.81.21.82`
throughout — the nameserver change moves *who answers DNS questions*, not
*where the site lives*. Nothing about the current site changes until the A
record is repointed deliberately, at the end.
