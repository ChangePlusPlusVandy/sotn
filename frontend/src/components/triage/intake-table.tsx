import { ROLE_LABELS, type Inquiry } from "./inquiry-labels";
import { StatusBadge } from "./status-badge";

// Fixed time zone so the server and browser render the same date.
const dateFormat = new Intl.DateTimeFormat("en-US", {
  month: "short",
  day: "numeric",
  year: "numeric",
  timeZone: "America/Chicago",
});

const COLUMNS = ["Name", "Group", "ZIP", "Status", "Submitted"];

export const IntakeRow = ({ inquiry }: { inquiry: Inquiry }) => {
  return (
    <tr className="border-b border-sotn-grey-light last:border-b-0">
      <td className="px-4 py-3.5">
        <p>{inquiry.contact_name}</p>
        <p className="mt-1 text-sotn-grey-dark">{inquiry.contact_email ?? inquiry.contact_phone}</p>
      </td>
      <td className="px-4 py-3.5">{ROLE_LABELS[inquiry.role]}</td>
      <td className="px-4 py-3.5">{inquiry.zip_code}</td>
      <td className="px-4 py-3.5">
        <StatusBadge status={inquiry.status} />
      </td>
      <td className="px-4 py-3.5 whitespace-nowrap">{dateFormat.format(new Date(inquiry.created_at))}</td>
    </tr>
  );
};

export const IntakeTable = ({ inquiries }: { inquiries: Inquiry[] }) => {
  return (
    <div className="overflow-x-auto rounded-xl border border-sotn-grey-light bg-white">
      <table className="w-full text-left text-sm leading-4">
        <thead className="border-b border-sotn-grey-light bg-sotn-biscuit text-sotn-grey-dark uppercase">
          <tr>
            {COLUMNS.map((column) => (
              <th key={column} scope="col" className="px-4 py-3 font-normal">
                {column}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {inquiries.length > 0 ? (
            inquiries.map((inquiry) => <IntakeRow key={inquiry.id} inquiry={inquiry} />)
          ) : (
            <tr>
              <td colSpan={COLUMNS.length} className="px-4 py-8 text-center text-sotn-grey-dark">
                No intakes match these filters.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};
