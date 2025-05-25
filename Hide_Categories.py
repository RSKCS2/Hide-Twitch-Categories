// ==UserScript==
// @name         Twitch: Hide Categories
// @namespace    https://twitch.tv/
// @version      1.3
// @run-at       document-start
// @description  Hide Twitch categories with an X, manage them in a dropdown panel with nice titles
// @match        https://www.twitch.tv/directory/following/live
// @grant        none
// ==/UserScript==

(function() {
  'use strict';

  const STORAGE_KEY = 'tm_blockedCategories';
  let blocked = loadBlocked();

  function loadBlocked() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
    } catch {
      return [];
    }
  }

  function saveBlocked(list) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(list));
  }

  function pruneBlocked() {
    document.querySelectorAll('a[data-test-selector="GameLink"]').forEach(link => {
      const href = link.getAttribute('href') || '';
      if (blocked.some(slug => href.includes(slug))) {
        const gridCell = link.closest('.live-channel-card')?.parentElement;
        if (gridCell) gridCell.remove();
      }
    });
  }

  function injectButtons() {
    document.querySelectorAll('a[data-test-selector="GameLink"]').forEach(link => {
      const href = link.getAttribute('href') || '';
      if (blocked.some(slug => href.includes(slug))) return;
      if (link.nextSibling?.classList?.contains('tm-hide-btn')) return;

      const match = href.match(/\/directory\/category\/([^\/]+)/);
      if (!match) return;
      const slug = match[1];

      const btn = document.createElement('span');
      btn.textContent = '×';
      btn.title = 'Hide this category';
      btn.className = 'tm-hide-btn';
      Object.assign(btn.style, {
        marginLeft: '4px',
        cursor: 'pointer',
        color: 'currentColor',
        fontWeight: 'bold',
      });

      btn.addEventListener('click', e => {
        e.stopPropagation();
        blocked.push(slug);
        saveBlocked(blocked);
        pruneBlocked();
        updatePanel();
      });

      link.parentElement.appendChild(btn);
    });
  }

  // transform slug "call-of-duty-black-ops-6" into "Call Of Duty Black Ops 6"
  function niceName(slug) {
    return slug
      .split('-')
      .map(s => s.charAt(0).toUpperCase() + s.slice(1))
      .join(' ');
  }

  function updatePanel() {
    const container = document.getElementById('tm-category-panel-list');
    if (!container) return;
    container.innerHTML = '';

    if (blocked.length === 0) {
      const none = document.createElement('div');
      none.textContent = 'No hidden categories';
      none.style.padding = '4px 0';
      container.appendChild(none);
      return;
    }

    blocked.forEach(slug => {
      const row = document.createElement('div');
      Object.assign(row.style, {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '2px 0'
      });

      const label = document.createElement('span');
      label.textContent = niceName(slug);
      label.style.flex = '1';

      const restoreBtn = document.createElement('button');
      restoreBtn.textContent = 'Unhide';
      Object.assign(restoreBtn.style, {
        marginLeft: '8px',
        fontSize: '12px',
        padding: '2px 6px',
        cursor: 'pointer',
      });

      restoreBtn.addEventListener('click', () => {
        blocked = blocked.filter(s => s !== slug);
        saveBlocked(blocked);
        updatePanel();
        pruneBlocked();
      });

      row.appendChild(label);
      row.appendChild(restoreBtn);
      container.appendChild(row);
    });
  }

  function addUI() {
    // toggle button
    const toggle = document.createElement('button');
    toggle.id = 'tm-panel-toggle';
    toggle.textContent = 'Hidden Categories ▼';
    Object.assign(toggle.style, {
      position: 'fixed',
      top: '60px',
      right: '12px',
      zIndex: '9999',
      background: '#9147ff',
      color: '#fff',
      border: 'none',
      padding: '6px 10px',
      borderRadius: '4px',
      cursor: 'pointer',
      fontSize: '13px'
    });

    // panel
    const panel = document.createElement('div');
    panel.id = 'tm-category-panel';
    Object.assign(panel.style, {
      position: 'fixed',
      top: '100px',
      right: '12px',
      width: '220px',
      background: '#18181b',
      color: '#fff',
      border: '1px solid #555',
      padding: '8px',
      borderRadius: '6px',
      fontSize: '13px',
      zIndex: '9999',
      display: 'none'
    });

    const header = document.createElement('div');
    header.textContent = 'Hidden Categories';
    header.style.fontWeight = 'bold';
    header.style.marginBottom = '6px';

    const container = document.createElement('div');
    container.id = 'tm-category-panel-list';

    panel.appendChild(header);
    panel.appendChild(container);
    document.body.append(toggle, panel);

    toggle.addEventListener('click', () => {
      const showing = panel.style.display === 'block';
      panel.style.display = showing ? 'none' : 'block';
      toggle.textContent = showing
        ? 'Hidden Categories ▼'
        : 'Hidden Categories ▲';
    });

    updatePanel();
  }

  function onMutations() {
    pruneBlocked();
    injectButtons();
    if (!document.getElementById('tm-panel-toggle')) {
      addUI();
    }
  }

  const obs = new MutationObserver(onMutations);
  obs.observe(document, { childList: true, subtree: true });

  if (document.readyState !== 'loading') {
    onMutations();
  } else {
    document.addEventListener('DOMContentLoaded', onMutations);
  }
})();
