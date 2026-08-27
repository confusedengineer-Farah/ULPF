import {
  LayoutDashboard,
  List,
  Plug,
  Settings,
} from "lucide-react";

function Sidebar({ activePage, setActivePage }) {
  const menuItems = [
    {
      name: "Dashboard",
      icon: LayoutDashboard,
    },
    {
      name: "Events",
      icon: List,
    },
    {
      name: "Sources",
      icon: Plug,
    },
    {
      name: "Settings",
      icon: Settings,
    },
  ];

  return (
    <aside className="w-56 min-h-screen bg-white border-r border-gray-200">

      <div className="px-5 py-5 border-b border-gray-200">
        <h1 className="text-xl font-semibold text-gray-900">
          ULPF
        </h1>

        <p className="text-xs text-gray-500 mt-1">
          Log Processing Framework
        </p>
      </div>

      <nav className="p-3">

        {menuItems.map((item) => {
          const Icon = item.icon;
          const active = activePage === item.name;

          return (
            <button
              key={item.name}
              onClick={() => setActivePage(item.name)}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-md mb-1 text-sm text-left ${
                active
                  ? "bg-gray-100 text-gray-900 font-medium"
                  : "text-gray-600 hover:bg-gray-50"
              }`}
            >
              <Icon size={18} />
              {item.name}
            </button>
          );
        })}

      </nav>

    </aside>
  );
}

export default Sidebar;