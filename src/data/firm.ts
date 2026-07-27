/**
 * Every fact about the firm, in one place.
 *
 * Nothing in this file may be invented. Each entry is either supplied by the
 * founder directly or verified against a source, and the source is noted where
 * it is not obvious. Anything still unknown is `null` and renders as a visible
 * [[חסר]] marker rather than being quietly omitted or guessed.
 *
 * The Bar's advertising rules are a CLOSED list — only what is enumerated there
 * may be published. Every field below was checked against it:
 *
 *   permitted: name, being a lawyer, academic degrees, address and all contact
 *   details, areas of practice, office hours, languages, date of admission,
 *   PREVIOUS LEGAL POSITIONS, teaching roles, articles written.
 *
 *   forbidden, and therefore absent by design: any reference to fees, any
 *   comparison to other lawyers, promised outcomes, success rates, and the word
 *   "מומחה" (there is no formal specialisation certification in Israel to
 *   justify it — the rules' own term is "תחומי עיסוק").
 */

export const FIRM = {
  name: 'עו״ד יהונתן שמם',
  /** The trade name. Not a separate legal entity — see `operator`. */
  legalName: 'משרד עו״ד יהונתן שמם',
  tagline: 'משרד בוטיק למשפט מסחרי וטכנולוגיה',

  /**
   * The registered person behind the trade name.
   *
   * Amendment 13 requires the controller to be identified with real
   * particulars, and "משרד עו״ד יהונתן שמם" is a trade name rather than a
   * registered entity. The migrated legal document names only the trade name,
   * which is thinner than the obligation expects.
   *
   * Same registration as the technology consultancy — one עוסק מורשה operating
   * under two trade names. That fact is what raises the additional-occupation
   * question recorded in PROJECT.md.
   */
  operator: {
    person: 'יהונתן שמם',
    registration: 'עוסק מורשה מס׳ 302910187',
    tradeName: 'משרד עו״ד יהונתן שמם',
  },

  phone: {
    display: '054-244-8885',
    tel: '+972542448885',
    // wa.me wants the number without + or separators
    whatsapp: '972542448885',
  },
  email: 'yonatan@shamam.net',
  calendar: 'https://calendar.app.google/LU3N8tPLz71vscQ68',
  linkedin: 'https://www.linkedin.com/in/yonatan-shamam-5b1892192/',

  address: {
    building: 'מגדלי אלון',
    street: 'יגאל אלון 94',
    city: 'תל אביב',
    country: 'IL',
    // Supersedes the "מגדלי הארבעה" on the live WordPress site, which is stale:
    // the move to Alon Towers is documented on the founder's own LinkedIn.
    full: 'מגדלי אלון, יגאל אלון 94, תל אביב',
  },

  hours: {
    // Sunday-Thursday, the Israeli working week.
    days: 'ראשון–חמישי',
    open: '09:00',
    close: '19:00',
    // schema.org openingHours, which wants English day codes and 24h times
    schema: ['Su', 'Mo', 'Tu', 'We', 'Th'].map((d) => `${d} 09:00-19:00`),
  },

  /** Explicitly permitted to publish. Supplied by the founder. */
  admittedYear: 2019,

  /** Explicitly permitted. */
  languages: ['עברית', 'אנגלית'],

  /**
   * Explicitly permitted: "תפקידים משפטיים קודמים".
   * Source: the founder's LinkedIn profile, supplied by him.
   */
  // Typed explicitly: without it, `as const` narrows each entry separately and
  // the optional `areas` is not on the union, so reading it fails to compile.
  previousRoles: [
    { role: 'עורך דין', org: 'גולדפרב זליגמן', from: 2019, to: 2022 },
    { role: 'מתמחה', org: 'משרד ש. הררי', from: 2018, to: 2019, areas: 'נדל״ן ודיני חברות' },
  ] as { role: string; org: string; from: number; to: number; areas?: string }[],

  /**
   * Academic degrees are explicitly permitted to publish and are a real
   * E-E-A-T signal. Supplied by the founder: Ono Academic College, 2018.
   *
   * The degree is stated as LL.B because an LL.B is a statutory precondition
   * for admission to the Israeli Bar, and he was admitted in 2019 — so this is
   * an entailment rather than a guess. If he in fact holds a different or
   * additional degree, correct it here.
   */
  education: [
    { degree: 'תואר ראשון במשפטים (LL.B)', institution: 'הקריה האקדמית אונו', year: 2018 },
  ],

  /** Regulation 35(ה) requires a named accessibility coordinator. */
  accessibilityCoordinator: {
    name: 'עו״ד יהונתן שמם',
    responseTime: 'עד 5 ימי עסקים',
  },

  /**
   * Physical accessibility of the office. Regulation 35 requires this in the
   * declaration, and it must describe the premises as they actually are —
   * a declaration that overstates is worse than one that admits a gap.
   *
   * Supplied by the founder on 27 Jul 2026. `null` means he has not stated it
   * and it renders as a visible gap rather than an assumption; the building is
   * a Tel Aviv high-rise so a lift certainly exists, but "certainly" is not a
   * basis for a statement in a legal document.
   */
  physicalAccess: {
    parking: false,
    approach: true,
    toilets: true,
    meetingRooms: true,
    entrance: null as boolean | null,
    lift: null as boolean | null,
  },
} as const;

/** Build a wa.me link with the message pre-filled for a specific service. */
export function whatsappLink(message?: string): string {
  const base = `https://wa.me/${FIRM.phone.whatsapp}`;
  return message ? `${base}?text=${encodeURIComponent(message)}` : base;
}
