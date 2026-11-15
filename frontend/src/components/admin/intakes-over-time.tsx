import type { DayCount } from "@/lib/admin-stats";

type IntakesOverTimeProps = {
  days: DayCount[];
};

/** Plain day-by-day counts until chart styling is designed. */
const IntakesOverTime = ({ days }: IntakesOverTimeProps) => {
  const max = Math.max(1, ...days.map((d) => d.count));

  return (
    <section className="border p-4">
      <h2 className="text-lg font-semibold">Intakes over time</h2>
      {days.length === 0 ? (
        <p className="mt-2 text-sm text-muted-foreground">No intakes in range.</p>
      ) : (
        <ul className="mt-4 space-y-2">
          {days.map(({ date, count }) => (
            <li key={date} className="grid grid-cols-[7rem_1fr_2rem] items-center gap-2">
              <span className="text-sm">{date}</span>
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

export default IntakesOverTime;
