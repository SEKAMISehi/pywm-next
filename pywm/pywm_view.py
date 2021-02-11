class PyWMView:
    def __init__(self, wm, handle):
        self._handle = handle

        """
        Consider these readonly
        """
        self.wm = wm
        self.parent = None
        self.floating = None
        self.title = None
        self.app_id = None
        self.role = None
        self.is_xwayland = None
        self.size_constraints = (0, 0, 0, 0)
        self.focused = False
        
        self.box = (0.0, 0.0, 1.0, 1.0)
        self.offset = (0, 0)
        self.size = (1, 1)
        self.z_index = 0
        self.accepts_input = True

        self._focus_pending = False
        self._resizing_pending = None
        self._fullscreen_pending = None
        self._maximized_pending = None
        self._size_pending = (-1, -1)


    def _update(self, 
                parent_handle,
                floating, title, app_id, role, is_xwayland, 
                sc_min_w, sc_max_w, sc_min_h, sc_max_h,
                offset_x, offset_y,
                size_w, size_h):
        if parent_handle is not None:
            for v in self.wm.views:
                if v._handle == parent_handle:
                    self.parent = v

        if floating is not None:
            self.floating = floating

        if title is not None:
            self.title = title

        if app_id is not None:
            self.app_id = app_id

        if role is not None:
            self.role = role

        if is_xwayland is not None:
            self.is_xwayland = is_xwayland

        if sc_min_w <= sc_max_w and sc_min_h <= sc_max_h:
            self.size_constraints = (sc_min_w, sc_max_w, sc_min_h, sc_max_h)

        if size_w > 0 and size_h > 0:
            self.size = (size_w, size_h)

        self.offset = (offset_x, offset_y)

        self.on_update()

        res = (
            self.box,
            self._focus_pending,
            -1 if self._resizing_pending is None else self._resizing_pending,
            -1 if self._fullscreen_pending is None else self._fullscreen_pending,
            -1 if self._maximized_pending is None else self._maximized_pending,
            self._size_pending,
            self.accepts_input, self.z_index)
        self._focus_pending = False
        self._resizing_pending = None
        self._fullscreen_pending = None
        self._maximized_pending = None
        self._size_pending = (-1, -1)
        return res


    def focus(self):
        self._focus_pending = True

    def set_resizing(self, val):
        self._resizing_pending = val

    def set_fullscreen(self, val):
        self._fullscreen_pending = val

    def set_maximized(self, val):
        self._maximized_pending = val

    def set_box(self, x, y, w, h):
        self.box = (float(x), float(y), float(w), float(h))

    def set_size(self, width, height):
        self.size = (int(width), int(height))
        self._size_pending = self.size

    def set_z_index(self, z_index):
        self.z_index = z_index

    def set_accepts_input(self, accepts_input):
        self.accepts_input = accepts_input

    
    """
    Virtual methods
    """
    def main(self):
        pass

    def on_update(self):
        pass

    def destroy(self):
        pass

    def on_focus_change(self):
        pass
