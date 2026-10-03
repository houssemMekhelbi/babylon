# ~/.config/zsh/babylon.zsh-theme
# Babylon prompt: standalone (no oh-my-zsh), no powerline blocks.
# Two lines: the context line, then the wedge.
#   status  crimson "✕ code", ⚡ root, ⚙ jobs; only when there is something to say
#   context muted user@host, only over SSH or as another user
#   dir     gold, bold (the shortened path)
#   git     lapis branch, crimson ± when dirty
#   prompt  a lit-gold ▸ on the second line; the clock sits right, dim
# Hex colours need zsh 5.7+ and a true-colour terminal.

setopt prompt_subst

BABYLON_DEFAULT_USER=${BABYLON_DEFAULT_USER:-$USER}   # hide context on your own box

S_TEXT='#F0E7D2'  S_STRUCT='#D4A72C' S_MUTED='#A99B80'
S_TAN='#7A6A4C'   S_SHU='#EB4B50'    S_AI='#7FA4E2'
S_LAMP='#F4D675'

# ~/dotfiles/hypr -> ~/d/hypr
babylon_short_pwd() {
  local p=${(%):-%~}
  local -a parts=("${(@s:/:)p}")
  local i
  for (( i = 1; i < ${#parts}; i++ )); do
    [[ -z ${parts[i]} || ${parts[i]} == '~' ]] && continue
    if [[ ${parts[i]} == .* ]]; then
      parts[i]=${parts[i][1,2]}
    else
      parts[i]=${parts[i][1]}
    fi
  done
  print -rn -- "${(j:/:)parts//\%/%%}"
}

babylon_status() {
  local -a s
  (( BABYLON_RETVAL != 0 )) && s+="✕ $BABYLON_RETVAL"
  (( UID == 0 )) && s+="⚡"
  [[ -n ${jobstates} ]] && s+="⚙"
  (( ${#s} )) && print -n "%F{$S_SHU}${(j: :)s}%f  "
}

babylon_context() {
  [[ $USER != $BABYLON_DEFAULT_USER || -n $SSH_CONNECTION ]] &&
    print -n "%F{$S_MUTED}%n@%m%f  "
}

babylon_dir() {
  print -n "%B%F{$S_STRUCT}$(babylon_short_pwd)%f%b"
}

babylon_git() {
  command git rev-parse --is-inside-work-tree &>/dev/null || return
  local ref
  ref=$(command git symbolic-ref --short HEAD 2>/dev/null) ||
    ref="➦ $(command git rev-parse --short HEAD 2>/dev/null)"
  ref=${ref//\%/%%}
  print -n "  %F{$S_AI}$ref%f"
  [[ -n $(command git status --porcelain --ignore-submodules=dirty 2>/dev/null | head -n1) ]] &&
    print -n "%F{$S_SHU} ±%f"
}

babylon_build_prompt() {
  babylon_status
  babylon_context
  babylon_dir
  babylon_git
}

babylon_precmd() { BABYLON_RETVAL=$? }
autoload -Uz add-zsh-hook
add-zsh-hook precmd babylon_precmd

PROMPT='%{%f%b%k%}$(babylon_build_prompt)
%F{$S_LAMP}▸%f '
RPROMPT="%F{$S_TAN}%*%f"

# ---- completion ------------------------------------------------------
autoload -Uz compinit && compinit
zstyle ':completion:*' menu select
zstyle ':completion:*' list-colors 'ma=48;2;212;167;44;38;2;11;9;8'

# ---- plugins ---------------------------------------------------------
ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE="fg=$S_TAN"
[[ -r /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh ]] &&
  source /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh

# zsh-syntax-highlighting must be sourced last, then styled.
if [[ -r /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh ]]; then
  source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
  ZSH_HIGHLIGHT_STYLES[command]='fg=#F0E7D2'
  ZSH_HIGHLIGHT_STYLES[builtin]='fg=#F0E7D2'
  ZSH_HIGHLIGHT_STYLES[alias]='fg=#F0E7D2'
  ZSH_HIGHLIGHT_STYLES[function]='fg=#F0E7D2'
  ZSH_HIGHLIGHT_STYLES[precommand]='fg=#F0E7D2,underline'
  ZSH_HIGHLIGHT_STYLES[path]='fg=#D4A72C,underline'
  ZSH_HIGHLIGHT_STYLES[single-hyphen-option]='fg=#7FA4E2'
  ZSH_HIGHLIGHT_STYLES[double-hyphen-option]='fg=#7FA4E2'
  ZSH_HIGHLIGHT_STYLES[single-quoted-argument]='fg=#9DBB6A'
  ZSH_HIGHLIGHT_STYLES[double-quoted-argument]='fg=#9DBB6A'
  ZSH_HIGHLIGHT_STYLES[unknown-token]='fg=#EB4B50,underline'
fi

export FZF_DEFAULT_OPTS="--color=bg+:#D4A72C,fg:#A99B80,fg+:#0B0908,hl:#D4A72C,hl+:#0B0908:underline,pointer:#0B0908,prompt:#F4D675,info:#A99B80,border:#D4A72C --pointer='▶' --prompt='▸ ' --border=sharp"
