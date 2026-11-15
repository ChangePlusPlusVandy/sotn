"use client";

import { useMemo, useState } from "react";
import { ChevronDown } from "lucide-react";
import { Button } from "@/components/ui/button";
import { IntakeTable } from "./intake-table";
import {
  ROLE_LABELS,
  STATUS_LABELS,
  type Inquiry,
  type InquiryRole,
  type InquiryStatus,
} from "./inquiry-labels";

const PAGE_SIZE = 12;

const fieldClass =
  "h-[42px] w-full rounded-xl border border-sotn-grey-light bg-white px-3 text-sm outline-none focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/50";

const FilterSelect = <T extends string>({
  label,
  value,
  allLabel,
  options,
  onChange,
}: {
  label: string;
  value: T | "";
  allLabel: string;
  options: Record<T, string>;
  onChange: (value: T | "") => void;
}) => {
  return (
    <label className="flex w-45 flex-col gap-2 text-sm text-sotn-grey-dark">
      {label}
      <span className="relative">
        <select
          value={value}
          onChange={(event) => onChange(event.target.value as T | "")}
          className={`${fieldClass} appearance-none pr-8 ${value ? "text-foreground" : "text-sotn-grey-mid"}`}
        >
          <option value="">{allLabel}</option>
          {(Object.entries(options) as [T, string][]).map(([optionValue, optionLabel]) => (
            <option key={optionValue} value={optionValue}>
              {optionLabel}
            </option>
          ))}
        </select>
        <ChevronDown className="pointer-events-none absolute top-1/2 right-3 size-4 -translate-y-1/2" />
      </span>
    </label>
  );
};

export const TriageList = ({ inquiries }: { inquiries: Inquiry[] }) => {
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState<InquiryStatus | "">("");
  const [role, setRole] = useState<InquiryRole | "">("");
  const [page, setPage] = useState(1);

  const filtered = useMemo(() => {
    const term = search.trim().toLowerCase();
    return inquiries.filter(
      (inquiry) =>
        (!status || inquiry.status === status) &&
        (!role || inquiry.role === role) &&
        (!term ||
          inquiry.contact_name.toLowerCase().includes(term) ||
          inquiry.contact_email?.toLowerCase().includes(term)),
    );
  }, [inquiries, search, status, role]);

  const pageCount = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  const start = (page - 1) * PAGE_SIZE;
  const visible = filtered.slice(start, start + PAGE_SIZE);

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-end gap-3">
        <label className="flex flex-1 flex-col gap-2 text-sm text-sotn-grey-dark">
          Search
          <input
            type="search"
            value={search}
            onChange={(event) => {
              setSearch(event.target.value);
              setPage(1);
            }}
            placeholder="Name or email…"
            className={`${fieldClass} text-foreground placeholder:text-sotn-grey-mid`}
          />
        </label>
        <FilterSelect
          label="Status"
          value={status}
          allLabel="All statuses"
          options={STATUS_LABELS}
          onChange={(value) => {
            setStatus(value);
            setPage(1);
          }}
        />
        <FilterSelect
          label="User group"
          value={role}
          allLabel="All groups"
          options={ROLE_LABELS}
          onChange={(value) => {
            setRole(value);
            setPage(1);
          }}
        />
      </div>

      <IntakeTable inquiries={visible} />

      <div className="flex items-center justify-between">
        <p className="text-sm text-sotn-grey-dark">
          {filtered.length > 0
            ? `Showing ${start + 1}–${start + visible.length} of ${filtered.length} intakes`
            : "No intakes"}
        </p>
        <div className="flex gap-2">
          <Button
            variant="outline"
            className="h-11 rounded-xl border-sotn-grey-light px-4 text-base"
            disabled={page <= 1}
            onClick={() => setPage(page - 1)}
          >
            ← Previous
          </Button>
          <Button
            variant="outline"
            className="h-11 rounded-xl border-sotn-grey-light px-4 text-base"
            disabled={page >= pageCount}
            onClick={() => setPage(page + 1)}
          >
            Next →
          </Button>
        </div>
      </div>
    </div>
  );
};
