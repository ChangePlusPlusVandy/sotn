type BreakdownItem = {
  label: string;
  count: number;
};

type BreakdownListProps = {
  title: string;
  items: BreakdownItem[];
  emptyLabel?: string;
};

/** Shared list for role / region / status breakdowns. */
const BreakdownList = ({
  title,
  items,
  emptyLabel = "No data in range.",
}: BreakdownListProps) => {
  const max = Math.max(1, ...items.map((item) => item.count));

  return (
    <section className="border p-4">
      <h2 className="text-lg font-semibold">{title}</h2>
      {items.length === 0 ? (
        <p className="mt-2 text-sm text-muted-foreground">{emptyLabel}</p>
      ) : (
        <ul className="mt-4 space-y-2">
          {items.map(({ label, count }) => (
            <li
              key={label}
              className="grid grid-cols-[1fr_minmax(4rem,40%)_2rem] items-center gap-2"
            >
              <span className="text-sm">{label}</span>
              <div className="h-3 bg-muted">
                <div
                  className="h-3 bg-foreground/40"
                  style={{ width: `${(count / max) * 100}%` }}
                />
              </div>
              <span className="text-right text-sm">{count}</span>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
};

export default BreakdownList;
