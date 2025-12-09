<script lang="ts">
    import { set } from "$lib/net/set";
    import { uploadFileToServer } from "$lib/net/fileset";
    import { browser } from "$app/environment";
    import type { HomePageData } from "$lib/types/homepage";
    import { get } from "$lib/net/get";

    let authenticated = browser && localStorage.getItem("auth_token") !== null; // Client variable, set to true if user is authenticated
    let status = "";

    function login() {
        set(
            "/site/login",
            {},
            usertoken, // No token needed for login
        ).then((response) => {
            if (response.status === "success") {
                status = "Login successful!";
                token = usertoken;
                browser && localStorage.setItem("auth_token", token);
                authenticated = true;
            } else {
                status = "Login failed. Please check your token.";
            }
        });
    }

    function addContact() {
        if (!data) return;
        data.siteConfig.general_footer.contact.push({
            text: "",
            href: "",
        });
        data = data; // Trigger reactivity
    }

    function addEvent() {
        if (!data) return;
        data.siteConfig.timeline.push({ event: "", year: 0 });
        data = data;
    }

    function addKnowledge() {
        if (!data) return;
        data.siteConfig.knowledge.push({
            name: "",
            percent: 0,
        });
        data = data;
    }

    function addHobby() {
        if (!data) return;

        data.siteConfig.hobbies.push({
            name: "",
            percent: 0,
        });
        data = data;
    }

    function addProject() {
        if (!data) return;

        data.siteConfig.projects.push({
            name: "",
            desc: "",
            img: "",
            input: undefined,
            url: "",
        });
        data = data; // Trigger reactivity
    }

    function updateWhoami(params: { text1: string; text2: string }) {
        set(
            "/siteconfig/admin/set/whoami",
            { text1: params.text1, text2: params.text2 },
            token,
        );
        status = "Who am I section updated.";
    }

    function uploadImageEvent(
        input: HTMLInputElement | undefined,
        data?: { img: string },
    ) {
        if (!input || !input.files || input.files.length === 0) {
            alert("No file selected.");
            return;
        }
        const file = input.files[0];
        const formData = new FormData();
        formData.append("file", file, file.name);

        uploadFileToServer("/site/images/upload", formData, token, data);
        status = "Uploading image...";
    }

    function updateHobbies(params: { name: string; percent: number }[]) {
        set("/siteconfig/admin/set/hobbies", params, token);
        status = "Hobbies updated.";
    }

    function updateKnowledge(params: { name: string; percent: number }[]) {
        set("/siteconfig/admin/set/knowledge", params, token);
        status = "Knowledge updated.";
    }

    function updateTimeline(params: { event: string; year: number }[]) {
        set("/siteconfig/admin/set/timeline", params, token);
        status = "Timeline updated.";
    }

    function updateFooterData(params: {
        contact: { text: string; href: string }[];
        git_url: string;
        name: string;
        footer_text: string;
    }) {
        set("/siteconfig/admin/set/general_footer", params, token);
        status = "Footer data updated.";
    }

    function updateProjects(
        params: {
            name: string;
            desc: string;
            img: string;
        }[],
    ) {
        for (const project of params) {
            delete (project as any).input;
        }
        set("/siteconfig/admin/set/projects", params, token);
        status = "Projects updated.";
    }

    let whoami_txt1 = "";
    let whoami_txt2 = "";
    let data: HomePageData | undefined = undefined;

    let token = (browser && localStorage.getItem("auth_token")) || "";

    let usertoken = "";

    if (authenticated) {
        get("/siteconfig/get/all").then((response) => {
            data = { siteConfig: response } as HomePageData;
            whoami_txt1 = data?.siteConfig.whoami.text1;
            whoami_txt2 = data?.siteConfig.whoami.text2;
        });
    }
</script>

<main>
    {#if status !== ""}
        <div class="notifications">
            <p id="status">{status}</p>
        </div>
    {/if}
    <h1>Admin Panel</h1>
    {#snippet upload_image(data: {
        img: string;
        input: HTMLInputElement | undefined;
    })}
        <input
            type="file"
            name="image"
            id="image"
            multiple
            bind:this={data.input}
        />
        <button on:click={() => uploadImageEvent(data.input, data)}
            >Upload Image</button
        >
    {/snippet}
    {#if authenticated}
        {#if data !== undefined}
            <label for="token">Auth Token (for testing purposes):</label>
            <input id="token" bind:value={token} />
            <section>
                <h2>Who am I section</h2>
                <label for="whoami_txt1">Who am I (1)?</label>
                <textarea
                    rows="4"
                    cols="50"
                    bind:value={whoami_txt1}
                    id="whoami_txt1"
                ></textarea>
                <label for="whoami_txt2">Who am I (2)?</label>
                <textarea
                    rows="4"
                    cols="50"
                    bind:value={whoami_txt2}
                    id="whoami_txt2"
                ></textarea>
                <button
                    on:click={() =>
                        updateWhoami({
                            text1: whoami_txt1,
                            text2: whoami_txt2,
                        })}>Save</button
                >
            </section>
            <section>
                <h2>Projects</h2>
                <ul>
                    {#each data.siteConfig.projects as project, index}
                        <li>
                            <h3>Project {index + 1}</h3>
                            <label for="project1_name">Project Name:</label>
                            <input
                                on:input={(e) =>
                                    (project.name = (
                                        e.target as HTMLInputElement
                                    ).value)}
                                value={project.name}
                                type="text"
                                id="project1_name"
                            />
                            <label for="project1_desc"
                                >Project Description:</label
                            >
                            <textarea
                                on:input={(e) =>
                                    (project.desc = (
                                        e.target as HTMLTextAreaElement
                                    ).value)}
                                id="project1_desc">{project.desc}</textarea
                            >
                            <label for="project1_url">Project URL:</label>
                            <input
                                on:input={(e) =>
                                    (project.url = (
                                        e.target as HTMLInputElement
                                    ).value)}
                                value={project.url}
                                type="text"
                                id="project1_url"
                            />
                            {@render upload_image(project)}
                        </li>
                    {/each}
                </ul>
                <button on:click={addProject}>Add</button>
                <button
                    on:click={() =>
                        data && updateProjects(data.siteConfig.projects)}
                    >Save</button
                >
            </section>
            <section>
                <h2>Hobbies</h2>
                <ul>
                    {#each data.siteConfig.hobbies as hobby, index}
                        <li>
                            <h3>Hobby {index + 1}</h3>
                            <label for="hobby1_name">Hobby Name:</label>
                            <input
                                on:input={(e) =>
                                    (hobby.name = (
                                        e.target as HTMLInputElement
                                    ).value)}
                                value={hobby.name}
                                type="text"
                                id="hobby1_name"
                            />
                            <label for="hobby1_percentage"
                                >Hobby Percentage:</label
                            >
                            <input
                                on:input={(e) =>
                                    (hobby.percent = parseInt(
                                        (e.target as HTMLInputElement).value,
                                    ))}
                                value={hobby.percent}
                                type="number"
                                id="hobby1_percentage"
                                min="0"
                                max="100"
                            />
                        </li>
                    {/each}
                </ul>
                <button on:click={addHobby}>Add</button>
                <button
                    on:click={() =>
                        data && updateHobbies(data.siteConfig.hobbies)}
                    >Save</button
                >
            </section>
            <section>
                <h2>Knowledge</h2>
                <ul>
                    {#each data.siteConfig.knowledge as know, index}
                        <li>
                            <h3>Knowledge {index + 1}</h3>
                            <label for="knowledge1_name">Knowledge Name:</label>
                            <input
                                on:input={(e) =>
                                    (know.name = (
                                        e.target as HTMLInputElement
                                    ).value)}
                                value={know.name}
                                type="text"
                                id="knowledge1_name"
                            />
                            <label for="knowledge1_percentage"
                                >Knowledge Percentage:</label
                            >
                            <input
                                on:input={(e) =>
                                    (know.percent = parseInt(
                                        (e.target as HTMLInputElement).value,
                                    ))}
                                value={know.percent}
                                type="number"
                                id="knowledge1_percentage"
                                min="0"
                                max="100"
                            />
                        </li>
                    {/each}
                </ul>
                <button on:click={addKnowledge}>Add</button>
                <button
                    on:click={() =>
                        data && updateKnowledge(data.siteConfig.knowledge)}
                    >Save</button
                >
            </section>
            <section>
                <h2>Timeline</h2>
                <ul>
                    {#each data.siteConfig.timeline as event, index}
                        <li>
                            <h3>Event {index + 1}</h3>
                            <label for="event1_title">Event Title:</label>
                            <input
                                on:input={(e) =>
                                    (event.event = (
                                        e.target as HTMLInputElement
                                    ).value)}
                                value={event.event}
                                type="text"
                                id="event1_title"
                            />
                            <label for="event1_year">Event Year:</label>
                            <input
                                on:input={(e) =>
                                    (event.year = parseInt(
                                        (e.target as HTMLInputElement).value,
                                    ))}
                                value={event.year}
                                type="number"
                                id="event1_year"
                            />
                        </li>
                    {/each}
                </ul>
                <button on:click={addEvent}>Add</button>
                <button
                    on:click={() =>
                        data && updateTimeline(data.siteConfig.timeline)}
                    >Save</button
                >
            </section>
            <section>
                <h2>Contact Info</h2>
                <ul>
                    {#each data.siteConfig.general_footer.contact as contact, index}
                        <li>
                            <h3>Contact Method {index + 1}</h3>
                            <label for="contact1_method">Contact Method:</label>
                            <input
                                on:input={(e) =>
                                    (contact.text = (
                                        e.target as HTMLInputElement
                                    ).value)}
                                value={contact.text}
                                type="text"
                                id="contact1_method"
                            />
                            <label for="contact1_value"
                                >Contact Value (href):</label
                            >
                            <input
                                on:input={(e) =>
                                    (contact.href = (
                                        e.target as HTMLInputElement
                                    ).value)}
                                value={contact.href}
                                type="text"
                                id="contact1_value"
                            />
                        </li>
                    {/each}
                </ul>
                <button on:click={addContact}>Add</button>
                <label for="giturl">Git URL:</label>
                <input
                    on:input={(e) =>
                        data &&
                        (data.siteConfig.general_footer.git_url = (
                            e.target as HTMLInputElement
                        ).value)}
                    value={data.siteConfig.general_footer.git_url}
                    type="text"
                    id="giturl"
                />
                <label for="name">Name:</label>
                <input
                    on:input={(e) =>
                        data &&
                        (data.siteConfig.general_footer.name = (
                            e.target as HTMLInputElement
                        ).value)}
                    value={data.siteConfig.general_footer.name}
                    type="text"
                    id="name"
                />
                <label for="footer_text">Footer text (small message):</label>
                <input
                    on:input={(e) =>
                        data &&
                        (data.siteConfig.general_footer.footer_text = (
                            e.target as HTMLInputElement
                        ).value)}
                    value={data.siteConfig.general_footer.footer_text}
                    type="text"
                    id="footer_text"
                />
                <button
                    on:click={() =>
                        data &&
                        updateFooterData(data.siteConfig.general_footer)}
                    >Save</button
                >
            </section>
        {/if}
    {:else}
        <p>You are not authorized to view this page.</p>
        <input type="text" placeholder="Auth Token" bind:value={usertoken} />
        <button on:click={login}>Login</button>
    {/if}
</main>

<style>
    .notifications {
        position: fixed;
        top: 10px;
        right: 10px;
        background-color: var(--bg-secondary);
        padding: 10px;
        border: 1px solid var(--border-primary);
        border-radius: 5px;
        z-index: 1000;
        max-width: 300px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }

    .notifications p {
        margin: 0;
        font-size: 0.9em;
        color: var(--text-primary);
        animation: notifEnter 0.3s ease-out;
    }

    section,
    li {
        display: flex;
        flex-direction: column;
    }

    textarea {
        resize: none;
    }

    main {
        background-color: var(--bg-primary);
        color: var(--text-primary);
        padding: 50px;
    }

    section {
        padding: 20px;
        border: 5px solid var(--border-primary);
        border-bottom: none;
    }

    section:last-of-type {
        border-bottom: 5px solid var(--border-primary);
    }

    textarea,
    input,
    button {
        background-color: var(--bg-secondary);
        color: var(--text-primary);
        border: 1px solid var(--border-primary);
        border-radius: 5px;
        padding: 5px;
        margin-bottom: 10px;
        font-family: var(--font-family);
    }

    button {
        cursor: pointer;
        transition: 0.3s;
    }

    button:hover {
        background-color: var(--bg-primary);
        transform: scale(1.01);
    }

    @keyframes notifEnter {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
</style>
