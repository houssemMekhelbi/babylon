-- Babylon look and feel.
-- The king's treasury: gold is line, never fill; the one selected thing is the
-- only solid gold on screen; crimson belongs to failure alone. Loaded after
-- futuwwa.lua so these values win; behaviour and binds stay there.
--
-- Windows are sharp black glass in a 1px gold line that runs from lit gold to
-- deep gold; the focused one stands in a faint gold light. The gates (ripples),
-- chains and cuneiform numerals live where we draw: the wallpaper, the bar, the
-- prayer banner, the lock screen, icons and cursor.

local C = {
    ground   = "0B0908",
    line     = "3A2E1A",
    gold     = "D4A72C",
    goldlit  = "F4D675",
    golddeep = "8E6B1F",
}

hl.config({
    general = {
        gaps_in     = 6,
        gaps_out    = 14,
        border_size = 1,
        col = {
            active_border   = {
                colors = { "rgb(" .. C.goldlit .. ")", "rgb(" .. C.gold .. ")", "rgb(" .. C.golddeep .. ")" },
                angle  = 45,
            },
            inactive_border = "rgb(" .. C.line .. ")",
        },
    },

    decoration = {
        rounding       = 0,
        rounding_power = 2.0,

        active_opacity   = 0.95,
        inactive_opacity = 0.88,

        blur = {
            enabled           = true,
            size              = 8,
            passes            = 3,
            vibrancy          = 0.08,
            noise             = 0.015,
            new_optimizations = true,
            popups            = true,
        },

        glow = {
            enabled = false,
        },

        -- Gold light around the focused window, plain black under the others.
        shadow = {
            enabled        = true,
            range          = 30,
            render_power   = 3,
            offset         = { 0, 0 },
            color          = "rgba(" .. C.gold .. "30)",
            color_inactive = "rgba(00000099)",
        },
    },

    group = {
        col = {
            border_active   = "rgb(" .. C.goldlit .. ")",
            border_inactive = "rgb(" .. C.line .. ")",
        },
    },

    misc = {
        disable_hyprland_logo    = true,
        disable_splash_rendering = true,
        background_color         = "rgb(" .. C.ground .. ")",
    },
})

-- Cursor: BabylonBlade (~/.local/share/icons/BabylonBlade, hyprcursor + XCursor).
-- On a live theme switch restore.sh runs `hyprctl setcursor` from gsettings.txt.
hl.env("HYPRCURSOR_THEME", "BabylonBlade")
hl.env("HYPRCURSOR_SIZE", "24")
hl.env("XCURSOR_THEME", "BabylonBlade")
hl.env("XCURSOR_SIZE", "24")

-- A config reload resets the cursor to the default theme; set it again.
local function babylon_cursor()
    hl.exec_cmd("hyprctl setcursor BabylonBlade 24")
end
hl.on("hyprland.start", babylon_cursor)
hl.on("config.reloaded", babylon_cursor)

-- Launcher bind points at the Babylon launcher; futuwwa.lua binds the Girih one.
hl.unbind("SUPER + D")
hl.bind("SUPER + D",
    hl.dsp.exec_cmd(os.getenv("HOME") .. "/.local/bin/babylon-launcher"),
    { description = "Application launcher" })

-- Terminals draw their own black glass (foot/alacritty/ghostty alpha) so text stays opaque.
hl.window_rule({
    name    = "babylon-terminal-opaque",
    match   = { class = "^(foot|footclient|Alacritty|com.mitchellh.ghostty)$" },
    opacity = "1.0 override 1.0 override",
})

-- Blur behind layer surfaces: the bar, alert banners, launcher, notifications.
-- ignore_alpha keeps fully transparent parts of a layer unblurred.
hl.layer_rule({
    name         = "babylon-bar-glass",
    match        = { namespace = "^hattin-" },
    blur         = true,
    ignore_alpha = 0.1,
})

hl.layer_rule({
    name         = "babylon-launcher-glass",
    match        = { namespace = "^launcher$" },
    blur         = true,
    ignore_alpha = 0.1,
})

hl.layer_rule({
    name         = "babylon-notify-glass",
    match        = { namespace = "^swaync" },
    blur         = true,
    ignore_alpha = 0.1,
})

-- Launcher: floating foot + fzf (~/.local/bin/babylon-launcher).
hl.window_rule({
    name     = "babylon-launcher",
    match    = { class = "^babylon-launcher$" },
    float    = true,
    size     = "780 470",
    center   = true,
    pin      = true,
    opacity  = "1.0 override 1.0 override",
})

-- Taskwarrior popups from the waybar "yawm" module (~/.local/bin/babylon-yawm).
hl.window_rule({
    name     = "babylon-yawm",
    match    = { class = "^babylon-yawm$" },
    float    = true,
    size     = "820 600",
    center   = true,
    pin      = true,
    opacity  = "1.0 override 1.0 override",
})

hl.window_rule({
    name     = "babylon-yawm-add",
    match    = { class = "^babylon-yawm-add$" },
    float    = true,
    size     = "720 240",
    center   = true,
    pin      = true,
    opacity  = "1.0 override 1.0 override",
})

local babylon_popups = { "babylon-launcher", "babylon-yawm", "babylon-yawm-add" }

-- Close every popup window except those of class `keep`.
-- hl.get_windows matches `class` exactly (no regex), so pass the plain name.
function babylon_close_popups(keep)
    for _, class in ipairs(babylon_popups) do
        if class ~= keep then
            for _, w in ipairs(hl.get_windows({ class = class })) do
                hl.dispatch(hl.dsp.window.close({ window = "address:" .. w.address }))
            end
        end
    end
end

function babylon_close_launcher()
    babylon_close_popups()
end

-- Close popups as soon as focus moves elsewhere.
hl.on("window.active", function(win)
    babylon_close_popups(win and win.class)
end)
