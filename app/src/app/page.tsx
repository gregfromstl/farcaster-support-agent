import {
    Frame,
    FrameButton,
    FrameConfig,
    FrameImage,
    FrameInput,
    FrameLink,
} from "@devcaster/next/frames";
import axios from "axios";

async function getResponse(query: string) {
    try {
        const response = await axios.post(
            "https://farcaster-support-agent.fly.dev",
            {
                message: query,
            },
            { timeout: 4000 }
        );
        return response.data.message;
    } catch {
        return "It took too long to answer that! Try again, or chat in Converse.";
    }
}

export default async function Home({
    searchParams,
}: {
    searchParams: Record<string, string>;
}) {
    const frame = new FrameConfig({ query: "" }, searchParams);

    let response = "";
    if (frame.state.query?.length > 0) {
        response = await getResponse(frame.state.query);
    }

    return (
        <>
            <Frame frame={frame}>
                <FrameImage
                    src={`${frame.origin}/image?query=${frame.state.query}&response=${response}`}
                />
                <FrameInput
                    placeholder={
                        frame.state.query?.length > 0
                            ? "Ask a followup..."
                            : "Type your question..."
                    }
                />
                <FrameLink href="https://converse.xyz/dm/0x0EDf09105b3875855F62bAEc1d8A412fDC7D607b">
                    Chat in Converse
                </FrameLink>
                <FrameButton
                    onClick={async (f: typeof frame) => {
                        f.state.query = f.action?.untrustedData.inputText!;
                    }}
                >
                    Submit
                </FrameButton>
            </Frame>
            <main className="flex min-h-screen flex-col items-center justify-between p-24"></main>
        </>
    );
}
