import { NextRequest } from "next/server";
import { NextResponse } from "next/server";
import { join } from "path";
import sharp from "sharp";
import fs from "fs";
import satori from "satori";
import { revalidatePath } from "next/cache";
export const dynamic = "force-dynamic";
export const revalidate = 0;

let semiboldFontData = fs.readFileSync(
    join(process.cwd(), "NunitoSansSemibold.ttf")
);
let fontData = fs.readFileSync(join(process.cwd(), "NunitoSansRegular.ttf"));

export async function GET(request: NextRequest) {
    revalidatePath(request.url);

    const searchParams = request.nextUrl.searchParams;
    const query = searchParams.get("query") || null;
    const response = searchParams.get("response") || null;

    const svg = await satori(
        <div
            style={{
                display: "flex",
                position: "relative",
                flexDirection: "row-reverse",
                width: "100%",
                height: "100%",
                backgroundColor: "white",
                color: "black",
            }}
        >
            <div
                style={{
                    display: "flex",
                    flex: 6,
                    flexDirection: "column",
                    padding: "54px 54px",
                    justifyContent: "space-between",
                }}
            >
                <div
                    style={{
                        display: "flex",
                        flexDirection: "column",
                        gap: "8px",
                    }}
                >
                    <h1
                        style={{
                            marginBottom: 0,
                            fontSize: "28px",
                            fontFamily: "semibold",
                        }}
                    >
                        {query ?? "Farcaster Support Agent"}
                    </h1>
                    <div
                        style={{
                            fontSize: "20px",
                            fontFamily: "normal",
                            color: "#303030",
                            display: "flex",
                        }}
                    >
                        {response ?? (
                            <div
                                style={{
                                    display: "flex",
                                    flexDirection: "column",
                                    gap: "12px",
                                }}
                            >
                                <div style={{ display: "flex" }}>
                                    This agent has been trained to answer your
                                    questions based on the Farcaster docs.
                                </div>
                                <div style={{ display: "flex" }}>
                                    Click "Chat in Converse" to talk to the
                                    agent via XMTP, powered by Operator.
                                </div>
                            </div>
                        )}
                    </div>
                </div>
                <div
                    style={{
                        display: "flex",
                        fontFamily: "normal",
                    }}
                >
                    Built by @gregfromstl
                </div>
            </div>
            <div
                style={{
                    display: "flex",
                    flex: 4,
                    backgroundColor: "#f2f2f2",
                    position: "relative",
                }}
            >
                <img
                    src="https://i.ibb.co/TTH7Grb/farcaster.png"
                    style={{
                        position: "absolute",
                        left: 0,
                        right: 0,
                        top: 0,
                        bottom: 0,
                        objectFit: "cover",
                        objectPosition: "center",
                    }}
                />
            </div>
        </div>,
        {
            width: 896,
            height: 469,
            fonts: [
                {
                    name: "semibold",
                    data: semiboldFontData,
                    weight: 600,
                    style: "normal",
                },
                {
                    name: "normal",
                    data: fontData,
                    weight: 400,
                    style: "normal",
                },
            ],
        }
    );

    // Convert SVG to PNG using Sharp
    const pngBuffer = await sharp(Buffer.from(svg)).toFormat("png").toBuffer();

    // Set the content type to PNG and send the response
    return new NextResponse(pngBuffer, {
        status: 200,
        headers: {
            "Content-Type": "image/png",
            "Cache-Control": "max-age=10",
        },
    });
}
