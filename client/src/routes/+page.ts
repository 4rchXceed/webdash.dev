import { get } from "$lib/net/get";

import type { LoadEvent } from "@sveltejs/kit";

export async function load({ fetch, params }: LoadEvent) {
    const siteConfig = await get("/siteconfig/get/all", fetch); // Verify authentication
    return { siteConfig };
}