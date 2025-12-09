export type HomePageData = {
    siteConfig: {
        projects: {
            name: string;
            desc: string;
            img: string;
            url: string;
            input: HTMLInputElement | undefined;
        }[];
        whoami: { text1: string; text2: string };
        hobbies: { name: string; percent: number }[];
        knowledge: { name: string; percent: number }[];
        timeline: { event: string; year: number }[];
        general_footer: {
            contact: { text: string; href: string }[];
            git_url: string;
            name: string;
            footer_text: string;
        };
    };
}