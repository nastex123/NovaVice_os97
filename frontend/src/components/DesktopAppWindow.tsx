import React from "react";
// Generic pluggable desktop window for OS97 registry (TODO-5.8).
export interface DesktopApp {
  id: string;
  title: string;
  render: () => React.ReactNode;
}
export const DesktopAppWindow: React.FC<{ app: DesktopApp }> = ({ app }) => (
  <section data-app={app.id} className="retro-window">
    <header className="retro-striped-titlebar">{app.title}</header>
    <div className="retro-window-body">{app.render()}</div>
  </section>
);
