---
title: 2 AM Hostel Chef: A Sarcastic Recipe Generator (Best Use of Gemma)
published: false
tags: devchallenge, weekendchallenge, hf26challenge
---

*This is a submission for the [Hacktoberfest Weekend Challenge: Build for a Friend](https://dev.to/challenges/hacktoberfest-weekend-2026-10-01)*

## What I Built
<!-- What does it do, and who is the friend or loved one you built it for?  What problem does it solve for them? -->
If you've ever lived in a student hostel, you know the 2 AM struggle. My friends constantly complain about being starving late at night, staring blankly at a random assortment of ingredients (like a banana, some stale muesli, and chili powder) and wondering what to do with it. They don't need a gourmet Michelin star cookbook; they need a chaotic, sarcastic chef that tells them exactly how to turn their random dorm room scraps into a meal using only a microwave. 

So for the Hacktoberfest Weekend Challenge, I built exactly that. Meet the **2 AM Hostel Chef**. It is a fully functioning Android APK (built with React and Capacitor) powered by a lightweight Python FastAPI backend hosted on Render. You type in whatever sad ingredients you have lying around, and the AI chef aggressively guides you through a recipe.

## Demo
<!-- Share a deployed link or a video demo. -->
{% youtube VqHSpgPugtw %}*

## Code
<!-- Show us the code!  You can embed a GitHub repo directly into your post. -->
The entire codebase (React Frontend, FastAPI backend, and GitHub Actions Android compilation) is completely open source:

{% github Rajeev-Kasyap/hacktoberfest26 %}

## How I Built It
<!-- Which open-source AI did you use (open-weight models, agent harnesses, frameworks, local inference), and how is your project built around it? -->
The core requirement of this project was to leverage an open-weight model. Initially, I tried running **Gemma 2B** locally via Ollama right on my laptop to make it a completely offline app. While it was incredibly fast, the 2 Billion parameter model struggled to maintain the strict JSON schema and sarcastic persona simultaneously (a phenomenon known as "attention collapse"). 

Because Gemma is open-weight and available everywhere, I was easily able to pivot my architecture without changing providers or prompts. I swapped my backend to hit Google AI Studio's massive **Gemma 4 26B** model. The jump in logic was staggering. The 26B model writes out an internal "Chain of Thought" before generating the recipe, resulting in flawless JSON schemas, hilarious Gen-Z sarcastic instructions, and actually edible recipes (it elegantly figured out how to use chili powder on a banana-muesli porridge!).

Having access to the open Gemma ecosystem meant I could start small on the edge for offline testing, and easily scale up to a colossal 26B cloud model when the reasoning required it.

The entire stack consists of:
* **Frontend:** React, Vite, TailwindCSS
* **Mobile Wrapper:** Capacitor (built to Android APK via GitHub Actions)
* **Backend:** Python FastAPI (hosted on Render's free tier)
* **AI Model:** `gemma-4-26b-a4b-it` (Google AI Studio)

## Why Does Open Innovation Matter?
<!-- Why does open innovation matter for what you built?  What did it make possible that a closed API wouldn't? -->
Open innovation meant I wasn't locked into a single inference provider. I was able to download the Gemma weights, run them locally on my own hardware using Ollama without needing the internet, experiment with the exact constraints of the model, and then seamlessly switch to Google's cloud API for the larger 26B parameter variant using the exact same underlying architecture. Closed APIs do not give you that freedom to experiment on the edge.

## Reactions & Suggestions
When I handed the app over to my friends, the reactions were hilarious. The aggressive, sarcastic tone of the AI chef was a massive hit. 

One major suggestion they had was to add a "Snap Photo" feature. They are far too lazy to actually type out the ingredients they have, so in a future update, I plan to integrate a multi-modal vision model where they can just point their phone camera at their messy desk, and the AI will auto-detect the food scraps!

Of course, even with flawless AI instructions, things can go wrong. Vamsi from my wing already managed to completely mess up his first attempt at a microwave porridge. But hey, the app can only give you the recipe—it can't cure being a genuinely terrible chef!

## Prize Categories
<!-- Which partner categories are you entering?  List every one that applies, or remove this section. -->
* Best Use of Gemma
* Best Use of Render

<!-- Team Submissions: Please pick one member to publish the submission and credit teammates by listing their DEV usernames directly in the body of the post. -->
*(No team members)*

<!-- Thanks for participating! -->
