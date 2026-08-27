import { useState } from "react";
import Sidebar from "./components/Sidebar";
import Dashboard from "./pages/Dashboard";

function App() {

  const [activePage, setActivePage] = useState("Dashboard");

  const renderPage = () => {

    if (activePage === "Dashboard") {
      return <Dashboard />;
    }

    return (
      <div className="p-8">

        <h2 className="text-2xl font-semibold text-gray-900">
          {activePage}
        </h2>

        <p className="text-sm text-gray-500 mt-2">
          This section will be implemented next.
        </p>

      </div>
    );
  };

  return (
    <div className="min-h-screen flex bg-gray-50">

      <Sidebar
        activePage={activePage}
        setActivePage={setActivePage}
      />

      <main className="flex-1">

        <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-8">

          <div>
            <p className="text-sm font-medium text-gray-800">
              Universal Log Pre-processing Framework
            </p>
          </div>

          <div className="flex items-center gap-2">

            <span className="w-2 h-2 rounded-full bg-green-500"></span>

            <span className="text-sm text-gray-600">
              Backend Online
            </span>

          </div>

        </header>

        {renderPage()}

      </main>

    </div>
  );
}

export default App;