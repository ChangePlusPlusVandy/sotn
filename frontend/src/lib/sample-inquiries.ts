import type { components } from "./api-types";

type Inquiry = components["schemas"]["InquiryRead"];

// Fake inquiries matching the backend's InquiryRead shape, newest first like GET /admin/inquiries.
// [name, role, status, zip, email, phone]
const ROWS: [string, Inquiry["role"], Inquiry["status"], string, string | null, string | null][] = [
  ["Aisha Robinson", "athlete", "new", "37902", "aisha.robinson@example.com", null],
  ["Ben Carter", "athlete", "needs_review", "37203", "ben.carter@example.com", "615-555-0142"],
  ["Chloe Nguyen", "volunteer", "assigned", "38103", "chloe.nguyen@example.com", null],
  ["Diego Alvarez", "volunteer", "contacted", "38501", "diego.alvarez@example.com", null],
  ["Elena Park", "partner", "referred", "37402", "elena.park@example.com", "423-555-0187"],
  ["Frankie Doyle", "partner", "new", "37604", null, "423-555-0110"],
  ["Gabby Suarez", "donor", "closed", "37064", "gabby.suarez@example.com", null],
  ["Henry Blake", "partner", "new", "38301", "henry.blake@example.com", null],
  ["Iris Chen", "athlete", "new", "38506", "iris.chen@example.com", null],
  ["Jonah Weiss", "volunteer", "needs_review", "37421", "jonah.weiss@example.com", null],
  ["Kaya Patel", "athlete", "assigned", "37919", "kaya.patel@example.com", "865-555-0133"],
  ["Liam O'Neill", "athlete", "contacted", "37211", "liam.o.neill@example.com", null],
  ["Maya Brooks", "athlete", "new", "38117", "maya.brooks@example.com", null],
  ["Noah Fields", "volunteer", "referred", "38583", "noah.fields@example.com", null],
  ["Olive Ramos", "partner", "needs_review", "37343", "olive.ramos@example.com", null],
  ["Priya Singh", "partner", "closed", "37620", "priya.singh@example.com", null],
  ["Quinn Larson", "donor", "new", "37027", "quinn.larson@example.com", "615-555-0199"],
  ["Ravi Bhatt", "partner", "assigned", "38305", "ravi.bhatt@example.com", null],
  ["Sasha Kim", "athlete", "needs_review", "38555", null, "931-555-0164"],
  ["Tomas Herrera", "volunteer", "contacted", "37411", "tomas.herrera@example.com", null],
  ["Uma Desai", "athlete", "referred", "37917", "uma.desai@example.com", null],
  ["Vera Popov", "athlete", "new", "37013", "vera.popov@example.com", null],
  ["Wes Ackerman", "athlete", "assigned", "38016", "wes.ackerman@example.com", null],
  ["Xio Vega", "volunteer", "closed", "38501", "xio.vega@example.com", null],
  ["Yasmin Hart", "volunteer", "new", "37405", "yasmin.hart@example.com", null],
  ["Zeke Morales", "partner", "contacted", "37601", "zeke.morales@example.com", null],
  ["Amelia Ford", "donor", "needs_review", "37067", "amelia.ford@example.com", null],
  ["Bruno Hall", "partner", "referred", "38134", "bruno.hall@example.com", null],
  ["Cora Yates", "athlete", "contacted", "38506", "cora.yates@example.com", null],
  ["Devi Rao", "volunteer", "new", "37415", "devi.rao@example.com", null],
];

const FIRST_SUBMITTED = Date.UTC(2026, 9, 19, 15);
const DAY_MS = 24 * 60 * 60 * 1000;

export const SAMPLE_INQUIRIES: Inquiry[] = ROWS.map(([name, role, status, zip, email, phone], index) => {
  const createdAt = new Date(FIRST_SUBMITTED - index * DAY_MS).toISOString();
  return {
    id: `00000000-0000-4000-8000-${String(index + 1).padStart(12, "0")}`,
    role,
    status,
    contact_name: name,
    contact_email: email,
    contact_phone: phone,
    zip_code: zip,
    answers: {},
    created_at: createdAt,
    updated_at: createdAt,
  };
});
