<script lang="ts">
    import { randomString } from "$lib/generalutils";
    import type { FooterData } from "$lib/types/Footer";

    export let scrollContainer: HTMLElement | undefined;
    export let isMounted: boolean[] | undefined;
    export let data: FooterData;

    let siteInfosElement: HTMLElement | null = null;
    let contactElement: HTMLElement | null = null;
    let alreadyListening = false;

    let lastScrollTop = 0;

    function animate(element: HTMLElement, first: number, second: number) {
        element.animate(
            [
                {
                    transform: `translateX(${first}%)`,
                    opacity: Math.abs(first) === 100 ? 0 : 1,
                },
                {
                    transform: `translateX(${second}%)`,
                    opacity: Math.abs(second) === 100 ? 0 : 1,
                },
            ],
            {
                duration: 500,
                easing: "ease",
                fill: "forwards",
            },
        );
    }

    function onScroll(target: HTMLElement) {
        const scrollTopPercent =
            (target.scrollTop / (target.scrollHeight - target.clientHeight)) *
            100;
        if (!siteInfosElement || !contactElement) return;
        if (scrollTopPercent > 95 && lastScrollTop <= target.scrollTop) {
            // Trigger animation only if not already running
            animate(siteInfosElement, -100, 0);
            animate(contactElement, 100, 0);
        } else if (lastScrollTop > target.scrollTop) {
            animate(siteInfosElement, 0, -100);
            animate(contactElement, 0, 100);
        }
        lastScrollTop = target.scrollTop;
    }

    $: {
        if (scrollContainer && isMounted && isMounted[0] && !alreadyListening) {
            alreadyListening = true;
            scrollContainer.addEventListener("scroll", () => {
                onScroll(scrollContainer);
            });
            onScroll(scrollContainer); // Initial check
        }
    }

    let footerData = {
        copyright: {
            beforeText: "~# ",
            texts: [
                { text: "© 2025 WebDash", isMouseOver: false, iId: -1 },
                {
                    text: `Created by <strong>${data.name}</strong>`,
                    isMouseOver: false,
                    iId: -1,
                }, // Hmm might not be the best solution, but it works for now
                { text: "MIT License", isMouseOver: false, iId: -1 },
            ],
        },
        siteSource: {
            beforeText: "~# ",
            texts: [
                {
                    text:
                        "<a style='color: inherit;' href='" +
                        data.git_url +
                        "' target='_blank'>Source Code</a>",
                    isMouseOver: false,
                    iId: -1,
                },
            ],
        },
        contact: {
            texts: data.contact,
        },
    };

    const beforeText = "~# ";
    function hideText(textData: { isMouseOver: boolean; iId: number }) {
        textData.isMouseOver = true;
        footerData = footerData; // Trigger reactivity
    }

    function showText(textData: { isMouseOver: boolean; iId: number }) {
        textData.isMouseOver = false;
        footerData = footerData;
    }
    function randomizeText(textData: { isMouseOver: boolean; iId: number }) {
        if (textData.isMouseOver && textData.iId === -1) {
            textData.iId = setInterval(() => {
                footerData = footerData;
            }, 50);
        } else if (!textData.isMouseOver && textData.iId !== -1) {
            clearTimeout(textData.iId);
            textData.iId = -1;
        }
    }

    $: {
        footerData.copyright.texts.forEach(randomizeText);
        footerData.siteSource.texts.forEach(randomizeText);
    }
</script>

{#snippet renderList(
    textData: { text: string; isMouseOver: boolean; iId: number }[],
)}
    <ul>
        {#each textData as textData}
            <li
                aria-hidden="true"
                on:mouseenter={(_e) => hideText(textData)}
                on:mouseleave={(_e) => showText(textData)}
            >
                <span class="before-text">{beforeText}</span>
                <span class="text">
                    {#if textData.isMouseOver}
                        {randomString(
                            Math.min(
                                Math.floor(textData.text.length / 1.5),
                                20,
                            ), // Usually, the random string is longer than the original text
                        )}
                    {:else}
                        {@html textData.text}
                    {/if}
                </span>
            </li>
        {/each}
    </ul>
{/snippet}
<footer class:no-hide={isMounted === undefined}>
    <section class="site_infos" bind:this={siteInfosElement}>
        <div class="copyright list">
            {@render renderList(footerData.copyright.texts)}
        </div>
        <div class="sitesource list">
            {@render renderList(footerData.siteSource.texts)}
        </div>
    </section>
    <div class="middle">
        <div class="content">
            <img
                src="/images/_homepage/HatsuneMiku_pjdiva.webp"
                alt="Easter Egg!"
            />
            <a
                target="_blank"
                href="https://miku.sega.com/megamixplus/index.html"
                >Image Copyright &copy; CFM</a
            >
            <p>
                <a
                    href={Math.random() < 0.5
                        ? "https://www.youtube.com/channel/UC8H4_odYb0aU8lJW1fWs5lw"
                        : "https://www.youtube.com/watch?v=F-bQgxWnmV4"}
                    target="_blank">Shoutout to a Vocaloid-P!</a
                >
                <!--
                Why doing this? 1st, I don't need a job, I'm still studying.
                 2nd, they deserve more recognition. 3rd, why not?
                  -->
            </p>
        </div>
    </div>
    <section class="contact" bind:this={contactElement}>
        <ul>
            {#each footerData.contact.texts as contact}
                <li>
                    <span class="before-text">&gt;</span>
                    <a
                        href={contact.href}
                        target="_blank"
                        rel="noopener noreferrer">{contact.text}</a
                    >
                </li>
            {/each}
        </ul>
        <div class="made-with">{data.footer_text}</div>
    </section>
</footer>

<style>
    a {
        color: var(--text-primary);
        text-decoration: underline;
        transition: 0.3s;
    }

    .middle {
        width: 10%;
    }

    .middle .content {
        transform: rotate3d(0, 1, 0, 180deg);
        backface-visibility: hidden;
        transition: 0.5s;
    }

    .middle .content img {
        border-radius: 10px;
        display: block;
        max-height: 100px;
        margin: auto;
        user-select: none;
        pointer-events: none;
    }

    .middle .content a {
        font-size: 0.6em;
    }

    .middle .content p {
        margin: 0;
        text-align: center;
    }

    .middle:hover .content {
        transform: rotate3d(0, 1, 0, 0deg);
    }

    .made-with {
        text-align: center;
        font-size: 0.8em;
        margin-top: 10px;
        color: gray;
    }

    footer {
        width: 100%;
        background-color: var(--bg-secondary);
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        color: var(--text-primary);
        overflow: hidden;
        align-items: stretch;
        border-top: 2px solid var(--border-primary);
    }

    .contact {
        display: flex;
        flex-direction: column;
        justify-content: space-around;
    }

    .contact ul {
        margin: 0;
        padding: 0;
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        list-style-type: none;
        padding-left: 10px;
        padding-bottom: 10px;
        border-bottom: 2px solid var(--border-primary);
    }

    .contact ul li {
        cursor: pointer;
        margin: 5px 0;
    }

    .contact ul li .before-text {
        margin-right: 10px;
        transition: 0.3s;
    }

    .contact ul li:hover > .before-text {
        margin-right: 20px;
    }

    .site_infos,
    .contact {
        width: 45%;
        box-sizing: border-box;
    }

    .site_infos {
        border-right: 2px solid var(--border-primary);
        padding-right: 10px;
        transform: translateX(-100%);
    }

    .contact {
        right: 0;
        border-left: 2px solid var(--border-primary);
        transform: translateX(100%);
    }

    footer.no-hide .site_infos,
    footer.no-hide .contact {
        transform: translateX(0%);
    }

    .copyright ul {
        border-bottom: 2px solid var(--border-primary);
    }

    .list ul {
        display: flex;
        flex-direction: column;
        justify-content: center;
        width: 100%;
        padding: 0;
        padding-left: 10px;
        list-style: none;
    }

    .list ul li {
        margin: 5px 0;
        display: flex;
        justify-content: flex-start;
        gap: 10px;
    }

    .list ul li span {
        cursor: pointer;
        user-select: none;
        transition: 0.3s;
    }

    .list ul li span.before-text {
        display: inline-block;
    }

    .list ul li span.text {
        display: inline-block;
        width: 80%;
    }

    @media screen and (max-width: 900px) {
        .middle {
            display: none;
        }
    }
</style>
