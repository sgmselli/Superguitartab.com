import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from "react-router-dom";

import { getTabData, downloadTab } from '../../api/tabs';
import { TabViewer } from './components/TabViewer';
import { Download } from 'lucide-react';
import { ContentNotFound } from '../../components/ContentNotFound';
import { Loading } from '../../components/Loading';
import type { TabResponse } from '../../types/tab';
import usePageTitle from '../../hooks/usePageTitle';
import { formatTitle } from '../../utils/wordFormatting';
import { useAuth } from '../../contexts/auth';
import { AuthRequiredModal } from '../../components/AuthRequiredModal';
import { DownloadedModal } from './components/DownloadedModal';

const Song: React.FC = () => {

    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();

    const [numPages, setNumPages] = useState<number>(0);

    const [song, setSong] = useState<TabResponse | null>(null);

    const [showAuthModal, setShowAuthModal] = useState<boolean>(false);
    const [showDownloadedModal, setShowDownloadedModal] = useState<boolean>(false);

    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    const { isAuthenticated } = useAuth();

    usePageTitle(song ? `${song.song_name} music tabular` : "Loading...");

    if (!id) {
        return <p>Invalid tab ID</p>;
    }

    const handleFetch = async () => {
        setLoading(true);
        setError(null);
        try {
            const data = await getTabData(id);
            setSong(data);
        } catch (err: any) {
            const detail = err?.response?.data?.detail;
            setError(typeof detail === "string" ? detail : "An error occurred");
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        handleFetch();
    }, [id])

    const handleDownload = async () => {
        if (!isAuthenticated()) {
            sessionStorage.setItem(
                "returnTo",
                location.pathname + location.search
            );
            setShowAuthModal(true);
            return;
        }

        try {
            const data = await downloadTab(id);
            const downloadable_file_url = data.file_url
            if (!downloadable_file_url) {
                return;
            }

            const response = await fetch(downloadable_file_url);
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);

            const link = document.createElement("a");
            link.href = url;

            link.download = song?.file_name || "superguitartab.com-tab";

            document.body.appendChild(link);
            link.click();

            link.remove();
            window.URL.revokeObjectURL(url);

            setShowDownloadedModal(true);

        } catch (error) {
            console.error("Download failed:", error);
        }
    }

    if (loading) {
        return (
            <div className='w-full h-[500px] flex items-center justify-center'>
                <Loading />
            </div>
        );
    }

    if (error) {
        return (
            <div className='flex flex-col items-center w-full mt-20 text-center'>
                <p className='text-error text-lg font-semibold'>{error}</p>
            </div>
        );
    }

    if (!song || !song.file_url) {
        return <ContentNotFound />;
    }

    return (
        <>
            <div
                className='flex flex-col lg:flex-row gap-10 pt-6'
            >
                <div className='flex-1 flex flex-col gap-4 lg:max-w-[540px]'>
                    <div className='lg:hidden flex flex-col justify-center items-center bg-gray-100 p-5 gap-4 rounded-lg'>
                        <h1 className='text-2xl primary-color font-semibold '>Download {song.song_name} now!</h1>
                        <button aria-label='Download song button for mobile' className='btn btn-lg w-full surface-color primary-color-bg rounded-lg' onClick={handleDownload}>Download tab</button>
                    </div>
                    <TabViewer pdfUrl={song.file_url} numPages={numPages} setNumPages={setNumPages} />
                </div>
                <div
                    className='flex-1 flex flex-col text-color'
                >
                    <div className='flex flex-col gap-2'>
                        <h1 className='text-4xl font-bold'>{song.song_name}</h1>
                        <h3 className='text-lg font-semibold'>Composed by <span className='font-bold'>{song.artist} </span>- Digital sheet tab</h3>
                    </div>

                    <p className='text-md font-light mt-3'>Includes unlimited printable PDF downloads</p>

                    <p className='text-md font-light mt-5' >{song.description}</p>

                    <div className='flex flex-row gap-4 mt-8'>
                        <button aria-label='Download song button' className='btn btn-xl flex flex-row gap-3 text-lg surface-color border-0 secondary-color-bg rounded-lg' onClick={handleDownload}><Download size={20} /> Download</button>
                    </div>

                    <div className='flex flex-row text-md gap-10 pt-8'>
                        <div className='flex flex-col font-semibold space-y-4'>
                            <p>Song:</p>
                            <p>Artist:</p>
                            <p>Album:</p>
                            <p>Genre:</p>
                            <p>Style:</p>
                            <p>Difficulty:</p>
                            <p>Lyrics included:</p>
                            <p>Pages:</p>
                            <p>Product #:</p>
                        </div>
                        <div className='flex flex-col space-y-4'>
                            <p>{song.song_name}</p>
                            <p>{song.artist ? song.artist : "No artist"}</p>
                            <p>{song.album ? song.album : "No album"}</p>
                            <p>{formatTitle(song.genre)}</p>
                            <p>{formatTitle(song.style)}</p>
                            <p>{song.difficulty}</p>
                            <p>{song.lyrics_included ? "Yes" : "No"}</p>
                            <p>{numPages}</p>
                            <p>{id}</p>
                        </div>

                    </div>
                </div>
            </div>
            <AuthRequiredModal
                isOpen={showAuthModal}
                onClose={() => setShowAuthModal(false)}
                onRegister={() => {
                    setShowAuthModal(false);
                    navigate('/register');
                }}
                onLogin={() => {
                    setShowAuthModal(false);
                    navigate('/login');
                }}
            />
            <DownloadedModal
                isOpen={showDownloadedModal}
                onClose={() => setShowDownloadedModal(false)}
                songName={song.song_name}
            />
        </>
    )
}


export default Song;