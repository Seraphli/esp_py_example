# Electron Spirit Plugin Example

ES 插件示例, python实现, 使用socket-io调用, 理论上可以使用任何支持socket-io的语言.

服务器接口说明

```typescript
export type PluginApiElement = {
  key: string;
  type: number;
  bound: { x: number; y: number; w: number; h: number };
  content: string;
};

export type PluginApiResponse = {
  code: number;
  msg: string;
};

export type PluginContext = {
  topic: string;
  pwd: string;
};

export interface ClientToServerEvents {
  echo: (msg: string) => void;
  register_topic: (ctx: PluginContext) => void;
  add_input_hook: (ctx: PluginContext, contentRegex: string) => void;
  del_input_hook: (ctx: PluginContext, contentRegex: string) => void;
  insert_css: (ctx: PluginContext, css: string) => void;
  remove_css: (ctx: PluginContext, key: string) => void;
  update_elem: (ctx: PluginContext, elem: PluginApiElement) => void;
  remove_elem: (ctx: PluginContext, elem: PluginApiElement) => void;
  show_view: (ctx: PluginContext, elem: PluginApiElement) => void;
  hide_view: (ctx: PluginContext, elem: PluginApiElement) => void;
  exec_js_in_elem: (
    ctx: PluginContext,
    elem: PluginApiElement,
    code: string,
  ) => void;
  notify: (
    ctx: PluginContext,
    text: string,
    title?: string,
    type?: 'success' | 'warn' | 'error',
    duration?: number,
  ) => void;
}

export interface ServerToClientEvents {
  echo: (resp: PluginApiResponse) => void;
  register_topic: (resp: PluginApiResponse) => void;
  add_input_hook: (resp: PluginApiResponse) => void;
  del_input_hook: (resp: PluginApiResponse) => void;
  insert_css: (resp: PluginApiResponse) => void;
  remove_css: (resp: PluginApiResponse) => void;
  update_elem: (resp: PluginApiResponse) => void;
  remove_elem: (resp: PluginApiResponse) => void;
  show_view: (resp: PluginApiResponse) => void;
  hide_view: (resp: PluginApiResponse) => void;
  exec_js_in_elem: (resp: PluginApiResponse) => void;
  notify: (resp: PluginApiResponse) => void;

  update_bound: (
    key: string,
    type: number,
    bound: { x: number; y: number; w: number; h: number },
  ) => void;
  process_content: (content: string) => void;
  mode_flag: (
    lock_flag: boolean,
    move_flag: boolean,
    dev_flag: boolean,
  ) => void;
  elem_activated: (key: string) => void;
  elem_deactivated: (key: string) => void;
  elem_remove: (key: string, callback: (cancel: boolean) => void) => void;
  elem_refresh: (key: string, callback: (cancel: boolean) => void) => void;
}
```