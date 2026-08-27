import { useEffect, useState } from "react";
import StatCard from "../components/StatCard";
import { getEventStats } from "../services/api";

function Dashboard() {

  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {

    const loadStats = async () => {

      try {

        const response = await getEventStats();

        if (response.success) {
          setStats(response.data);
        } else {
          setError("Could not load statistics.");
        }

      } catch (err) {

        console.error(err);
        setError("Backend server is not available.");

      } finally {

        setLoading(false);

      }
    };

    loadStats();

  }, []);

  if (loading) {
    return (
      <div className="p-8">
        <p className="text-gray-500">
          Loading dashboard...
        </p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-8">
        <div className="bg-white border border-red-200 rounded-lg p-5">
          <p className="text-red-600">
            {error}
          </p>
        </div>
      </div>
    );
  }

  const formats = stats?.formats || {};
  const plugins = stats?.plugins || {};
  const actions = stats?.actions || {};

  return (
    <div className="p-8">

      <div className="mb-7">

        <h2 className="text-2xl font-semibold text-gray-900">
          Dashboard
        </h2>

        <p className="text-sm text-gray-500 mt-1">
          Overview of processed security events
        </p>

      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">

        <StatCard
          title="Total Events"
          value={stats?.total_events ?? 0}
          description="Events stored in ULPF"
        />

        <StatCard
          title="CEF Events"
          value={formats.cef ?? 0}
          description="CEF format events"
        />

        <StatCard
          title="Syslog Events"
          value={formats.syslog ?? 0}
          description="Syslog format events"
        />

        <StatCard
          title="CSV Events"
          value={formats.csv ?? 0}
          description="CSV format events"
        />

      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 mt-6">

        <div className="bg-white border border-gray-200 rounded-lg p-5">

          <h3 className="font-medium text-gray-900">
            Event Formats
          </h3>

          <div className="mt-4 space-y-3">

            {Object.entries(formats).map(([format, count]) => (

              <div
                key={format}
                className="flex justify-between items-center"
              >
                <span className="text-sm text-gray-600 uppercase">
                  {format}
                </span>

                <span className="text-sm font-medium">
                  {count}
                </span>
              </div>

            ))}

          </div>

        </div>

        <div className="bg-white border border-gray-200 rounded-lg p-5">

          <h3 className="font-medium text-gray-900">
            Event Actions
          </h3>

          <div className="mt-4 space-y-3">

            {Object.entries(actions).map(([action, count]) => (

              <div
                key={action}
                className="flex justify-between items-center"
              >
                <span className="text-sm text-gray-600">
                  {action}
                </span>

                <span className="text-sm font-medium">
                  {count}
                </span>
              </div>

            ))}

          </div>

        </div>

      </div>

      <div className="bg-white border border-gray-200 rounded-lg p-5 mt-6">

        <h3 className="font-medium text-gray-900">
          Detected Plugins
        </h3>

        <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-3">

          {Object.entries(plugins).map(([plugin, count]) => (

            <div
              key={plugin}
              className="border border-gray-100 rounded-md p-3 flex justify-between"
            >
              <span className="text-sm text-gray-600">
                {plugin}
              </span>

              <span className="text-sm font-medium">
                {count}
              </span>
            </div>

          ))}

        </div>

      </div>

    </div>
  );
}

export default Dashboard;