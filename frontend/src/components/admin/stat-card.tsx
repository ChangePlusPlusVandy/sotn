type StatCardProps = {
  label: string;
  value: number | string;
  hint?: string;
};

/** Simple metric tile for the Overview dashboard. Styling is intentionally minimal. */
const StatCard = ({ label, value, hint }: StatCardProps) => {
  return (
    <div className="border p-4">
      <p className="text-sm uppercase tracking-wide text-muted-foreground">
        {label}
      </p>
      <p className="mt-2 text-3xl font-semibold">{value}</p>
      {hint ? <p className="mt-1 text-sm text-muted-foreground">{hint}</p> : null}
    </div>
  );
};

export default StatCard;
