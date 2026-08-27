function StatCard({ title, value, description }) {
  return (
    <div className="bg-white border border-gray-200 rounded-lg p-5">

      <p className="text-sm text-gray-500">
        {title}
      </p>

      <p className="text-2xl font-semibold text-gray-900 mt-2">
        {value}
      </p>

      {description && (
        <p className="text-xs text-gray-500 mt-2">
          {description}
        </p>
      )}

    </div>
  );
}

export default StatCard;