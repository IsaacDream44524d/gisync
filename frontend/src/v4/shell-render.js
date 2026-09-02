// Gentelella 2026 v4 — shell render (pure)
// String-only renderers. No DOM, no window/document access.
// Imported by:
//   1. The Vite plugin (vite.config.js) to inject shell HTML at build/dev time.
//   2. src/v4/shell.js as a runtime fallback for pages that bypass the plugin.

// NAV items are either flat — { key, href, text, icon, badge? } —
// or a parent with `children: [{ key, href, text, badge? }]` for a submenu.
// The parent is `key`-less; its children carry their own keys for the
// `data-page` highlight match. The parent stays expanded if any child matches.
export const PRONAV = [
  {
    label: 'General',
    items: [
      {
        text: 'Dashboards', icon: 'dashboard', href: window.ROUTES.dashboard
      },
      { key: 'calendar', href: window.ROUTES.calendar, text: 'Calendar', icon: 'calendar' }
    ]
  },
  {
    label: 'Apps',
    items: [
      { key: 'kanban', href: window.ROUTES.workflow, text: 'Kanban', icon: 'kanban' },
      { key: 'files', href: window.ROUTES.fileManagement, text: 'Files', icon: 'files' },
      { key: 'notifications', href: window.ROUTES.notifications, text: 'Notifications', icon: 'bell' }
    ]
  },
  {
    label: 'Admin',
    items: [
      // { key: 'users',           href: window.ROUTES.class,         text: 'Contacts',        icon: 'users' },
      { key: 'user_management', href: window.ROUTES.userManagement, text: 'User management', icon: 'profile' },
      { key: 'profile', href: window.ROUTES.profile, text: 'Your profile', icon: 'profile' },
      { key: 'settings', href: window.ROUTES.settings, text: 'Settings', icon: 'settings' },
      { key: 'faq', href: window.ROUTES.faq, text: 'Help center', icon: 'help' }
    ]
  },
];

// MVP dashboard, later switch back to PRO-NAV


export const NAV = [
  {
    label: 'General',
    items: [
      {
        text: 'Dashboards', icon: 'dashboard', href: window.ROUTES.class_rep_dashboard
      },
      { key: 'students', href: window.ROUTES.students, text: 'Students', icon: 'students' },
      { key: 'Groups', href: window.ROUTES.groups, text: 'Groups', icon: 'groups' }
    ]
  },
]

export const ICONS = {
  groups: '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-people" viewBox="0 0 16 16"><path d="M15 14s1 0 1-1-1-4-5-4-5 3-5 4 1 1 1 1zm-7.978-1L7 12.996c.001-.264.167-1.03.76-1.72C8.312 10.629 9.282 10 11 10c1.717 0 2.687.63 3.24 1.276.593.69.758 1.457.76 1.72l-.008.002-.014.002zM11 7a2 2 0 1 0 0-4 2 2 0 0 0 0 4m3-2a3 3 0 1 1-6 0 3 3 0 0 1 6 0M6.936 9.28a6 6 0 0 0-1.23-.247A7 7 0 0 0 5 9c-4 0-5 3-5 4q0 1 1 1h4.216A2.24 2.24 0 0 1 5 13c0-1.01.377-2.042 1.09-2.904.243-.294.526-.569.846-.816M4.92 10A5.5 5.5 0 0 0 4 13H1c0-.26.164-1.03.76-1.724.545-.636 1.492-1.256 3.16-1.275ZM1.5 5.5a3 3 0 1 1 6 0 3 3 0 0 1-6 0m3-2a2 2 0 1 0 0 4 2 2 0 0 0 0-4"/></svg>',
  students: '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-people-fill" viewBox="0 0 16 16"><path d="M7 14s-1 0-1-1 1-4 5-4 5 3 5 4-1 1-1 1zm4-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6m-5.784 6A2.24 2.24 0 0 1 5 13c0-1.355.68-2.75 1.936-3.72A6.3 6.3 0 0 0 5 9c-4 0-5 3-5 4s1 1 1 1zM4.5 8a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5"/></svg>',
  dashboard: '<svg class="icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="4" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="10" width="7" height="11" rx="1.5"/></svg>',
  ui: '<svg class="icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4 6h16M4 12h16M4 18h10"/></svg>',
  pages: '<svg class="icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="2" y="3" width="20" height="18" rx="2"/><path d="M2 8h20"/></svg>',
  users: '<svg class="icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="8" r="4"/><path d="M5 20c0-3.9 3.1-7 7-7s7 3.1 7 7"/></svg>',
  profile: '<svg class="icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
  settings: '<svg class="icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M5.6 18.4l2.1-2.1M16.3 7.7l2.1-2.1"/></svg>',
  chat: '<svg class="icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M21 11.5a8.38 8.38 0 01-.9 3.8 8.5 8.5 0 01-7.6 4.7 8.38 8.38 0 01-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 01-.9-3.8 8.5 8.5 0 014.7-7.6 8.38 8.38 0 013.8-.9h.5a8.48 8.48 0 018 8v.5z"/></svg>',
  bell: '<svg class="icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 3a6 6 0 00-6 6c0 6-3 7-3 7h18s-3-1-3-7a6 6 0 00-6-6z"/><path d="M10.5 21a1.5 1.5 0 003 0"/></svg>',
  kanban: '<svg class="icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="6" height="14" rx="1.5"/><rect x="11" y="3" width="6" height="9" rx="1.5"/><rect x="19" y="3" width="2" height="6" rx="0.5"/></svg>',
  files: '<svg class="icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 7a2 2 0 012-2h4l2 2h7a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V7z"/></svg>',
  help: '<svg class="icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><path d="M9.1 9a3 3 0 015.8 1c0 2-3 3-3 3"/><circle cx="12" cy="17" r="0.5" fill="currentColor"/></svg>',
  mail: '<svg class="icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="2" y="4" width="20" height="16" rx="3"/><path d="M2 7l10 6 10-6"/></svg>',
  projects: '<svg class="icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/></svg>',
  type: '<svg class="icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="4 7 4 4 20 4 20 7"/><line x1="9" y1="20" x2="15" y2="20"/><line x1="12" y1="4" x2="12" y2="20"/></svg>',
  icons: '<svg class="icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><path d="M8 14s1.5 2 4 2 4-2 4-2M9 9h.01M15 9h.01"/></svg>',
  layout: '<svg class="icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 9v12"/></svg>',
  code: '<svg class="icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M16 18l6-6-6-6M8 6l-6 6 6 6"/></svg>',
  paint: '<svg class="icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M19 11H5a2 2 0 00-2 2v2a2 2 0 002 2h2v3a1 1 0 001 1h3a1 1 0 001-1v-3h7a2 2 0 002-2v-2a2 2 0 00-2-2z"/><path d="M19 11V5a2 2 0 00-2-2h-2a2 2 0 00-2 2v6"/></svg>',
  calendar: '<svg class="icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 10h18M8 4v6M16 4v6"/></svg>',
};

const CHEVRON = '<svg class="nav-chev" width="12" height="12" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M6 4l4 4-4 4"/></svg>';

function renderNavItem(item, activeKey) {
  if (item.children) {
    const childActive = item.children.some((c) => c.key === activeKey);
    const sub = item.children.map((c) => {
      const a = c.key === activeKey;
      return `<a class="nav-sublink${a ? ' active' : ''}" href="${c.href}"${a ? ' aria-current="page"' : ''}>${c.text}${c.badge ? `<span class="badge ${c.badge.cls}">${c.badge.text}</span>` : ''}</a>`;
    }).join('');
    const cls = ['nav-tree'];
    if (childActive) { cls.push('open', 'has-active'); }
    return `
      <div class="${cls.join(' ')}">
        <button type="button" class="nav-link nav-toggle" aria-expanded="${childActive ? 'true' : 'false'}">
          ${ICONS[item.icon] || ''}
          <span class="nav-text">${item.text}</span>
          ${item.badge ? `<span class="badge ${item.badge.cls}">${item.badge.text}</span>` : ''}
          ${CHEVRON}
        </button>
        <div class="nav-sub"><div class="nav-sub-inner">${sub}</div></div>
      </div>
    `;
  }
  const a = item.key === activeKey;
  return `
    <a class="nav-link${a ? ' active' : ''}" href="${item.href}"${a ? ' aria-current="page"' : ''}>
      ${ICONS[item.icon] || ''}
      <span class="nav-text">${item.text}</span>
      ${item.badge ? `<span class="badge ${item.badge.cls}">${item.badge.text}</span>` : ''}
    </a>
  `;
}

export function renderSidebar(activeKey) {
  const groups = NAV.map((group) => `
    <div class="nav-group">
      <div class="nav-label">${group.label}</div>
      ${group.items.map((item) => renderNavItem(item, activeKey)).join('')}
    </div>
  `).join('');

  // put username here
  return `
    <aside class="sidebar" aria-label="Primary navigation">
      <div class="sidebar-brand">
        <div class="brand-icon">G</div>
        <div class="brand-name">GISync<small>V1.0</small></div>
      </div>
      <nav class="sidebar-nav">${groups}</nav>
      <div class="sidebar-footer">
        <div class="sidebar-user">
          <div class="avatar">${window.USER.username[0]}</div>
          <div class="sidebar-user-info">
            <div class="name">${window.USER.username}</div>
            <div class="role">${window.USER.role}</div>
          </div>
          <button class="more-btn" aria-label="More options">
            <svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor"><circle cx="8" cy="3" r="1.2"/><circle cx="8" cy="8" r="1.2"/><circle cx="8" cy="13" r="1.2"/></svg>
          </button>
        </div>
      </div>
    </aside>
  `;
}

export function renderTopbar(breadcrumb) {
  const crumbs = (breadcrumb || ['Home']).map((c, i, arr) => {
    const isLast = i === arr.length - 1;
    return `${i > 0 ? '<span class="sep" aria-hidden="true">›</span>' : ''}<span${isLast ? ' class="current" aria-current="page"' : ''}>${c}</span>`;
  }).join('');

  // info for header buttons
  return `
    <header class="topbar">
      <div class="topbar-left">
        <button class="sidebar-toggle" type="button" aria-label="Open menu" aria-controls="sidebar" aria-expanded="false">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
        </button>
        <nav class="breadcrumb" aria-label="Breadcrumb">${crumbs}</nav>
      </div>
      <div class="search-box">
        <svg class="s-icon" width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="7" cy="7" r="5"/><path d="M11 11l3.5 3.5"/></svg>
        <input type="text" placeholder="Search for anything…" aria-label="Open command palette">
        <kbd>⌘K</kbd>
      </div>
      <div class="topbar-right">
        <button class="tb-avatar" type="button" aria-label="Account menu" aria-haspopup="menu" aria-expanded="false">I</button>
      </div>
    </header>
  `;
}

export function renderFooter() {
  return `
    <footer class="footer">
      <span>GISync — An academic resource platform for GIS students by <a href="#">REALM Tech</a></span>
    </footer>
  `;
}

export function renderShell({ activeKey = '', breadcrumb = ['Home'] } = {}) {

  return {
    sidebar: renderSidebar(activeKey),
    topbar: renderTopbar(breadcrumb),
    footer: renderFooter()
  };
}

export function parseShellAttrs(attrs) {
  const shell = /data-shell\s*=\s*["']([^"']*)["']/.exec(attrs);
  if (!shell || shell[1] !== 'admin') { return null; }
  const page = /data-page\s*=\s*["']([^"']*)["']/.exec(attrs);
  const bc = /data-breadcrumb\s*=\s*["']([^"']*)["']/.exec(attrs);
  return {
    activeKey: page ? page[1] : '',
    breadcrumb: bc ? bc[1].split('>').map((s) => s.trim()).filter(Boolean) : ['Home']
  };
}
