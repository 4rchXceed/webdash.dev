<script lang="ts">
	import favicon from "$lib/assets/favicon.svg";
	import Footer from "./footer.svelte";
	import { page } from "$app/state";
	import "../vars.css";
	import { get } from "$lib/net/get";
	import type { FooterData } from "$lib/types/footer";

	let footerData: FooterData = {
		contact: [
			{
				text: "Contact me",
				href: "mailto:lyam.zambaz@edu.vs.ch",
			},
		],
		git_url: "https://github.com/ArchXceed",
		name: "WebDash",
		footer_text: "© 2025 WebDash",
	};

	get("/siteconfig/get/all").then((data: FooterData) => {
		footerData.footer_text = data.footer_text;
		footerData.name = data.name;
		footerData.git_url = data.git_url;
		footerData.contact = data.contact;
	});

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<div class="content">
	{@render children?.()}
	{#if page.url.pathname !== "/"}
		<!-- No footer on home page -->
		{#if footerData.contact.length > 0}
			<!-- Only show footer if contact info is available -->
			<Footer
				scrollContainer={undefined}
				isMounted={undefined}
				data={footerData}
			/>
		{/if}
	{/if}
</div>

<style>
	.content {
		scroll-behavior: smooth;
		position: absolute;
		font-family: var(--font-family);
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		margin: 0;
		padding: 0;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
	}
</style>
