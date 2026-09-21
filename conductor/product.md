# Conductor Plugin

**Measure twice, code once.**

Conductor is a Spec-Driven Development plugin for AI coding agents (Cursor,
Claude Code, and Antigravity). It turns the agent into a project manager that
follows Context → Spec & Plan → Implement for every feature, bug, and chore.

This repository is the plugin itself. The fork at `swainjo/conductor` dogfoods
Linear-first tracks locally while contributing plugin skills back to
`gemini-cli-extensions/conductor`.

## Users

- Plugin contributors shipping skills, rules, and Linear-first / GitHub-first behavior
- Agent users who install Conductor into their own product repos

## Goals

- Keep SDD protocols precise, sequential, and host-adaptive
- File-based specs by default; Linear-first when `conductor/linear.md` exists;
  GitHub-first when `conductor/github.md` exists (not both)
- Dogfood Linear tracks on this fork without leaking that workspace into
  upstream PRs

## Core capabilities

- Setup, new-track, implement, status, revert, review
- Optional Linear-first or GitHub-first: issue as spec, pointer tracks,
  handoff/review/label skills
- Style guides and workflow templates copied into consuming projects
